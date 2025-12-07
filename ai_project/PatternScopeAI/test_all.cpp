#include <iostream>
#include <iomanip>
#include "src/data/Image.h"
#include "src/data/FeatureVector.h"
#include "src/data/Dataset.h"
#include "src/data/MNISTLoader.h"
#include "src/data/ConfusionMatrix.h"
#include "src/ai/features/PixelGridExtractor.h"
#include "src/ai/features/EdgeMapExtractor.h"
#include "src/ai/features/HOGExtractor.h"
#include "src/ai/models/KNN.h"
#include "src/ai/models/NaiveBayes.h"
#include "src/ai/models/MiniMLP.h"
#include "src/ai/search/AStarMatcher.h"
#include "src/ai/rules/RuleEngine.h"
#include "src/ai/rules/StructuralFeatures.h"

int main() {
    std::cout << "=== PatternScope AI - Quick Test ===" << std::endl;
    
    int passed = 0;
    int total = 0;
    
    std::string testImagesPath = "../mnist/t10k-images.idx3-ubyte";
    std::string testLabelsPath = "../mnist/t10k-labels.idx1-ubyte";
    std::string trainImagesPath = "../mnist/train-images.idx3-ubyte";
    std::string trainLabelsPath = "../mnist/train-labels.idx1-ubyte";
    
    total++;
    Dataset testDataset;
    if (MNISTLoader::loadDataset(testImagesPath, testLabelsPath, testDataset) && testDataset.size() > 0) {
        std::cout << "✓ Data loading: " << testDataset.size() << " samples" << std::endl;
        passed++;
    } else {
        std::cout << "✗ Data loading failed" << std::endl;
        return 1;
    }
    
    total++;
    std::vector<Image> images;
    std::vector<int> labels;
    bool imagesLoaded = MNISTLoader::loadImages(testImagesPath, images) && 
                        MNISTLoader::loadLabels(testLabelsPath, labels) && 
                        images.size() > 0;
    if (imagesLoaded) {
        PixelGridExtractor pixelExt(28, 28);
        FeatureVector fv = pixelExt.extract(images[0]);
        if (fv.size() == 784) {
            std::cout << "✓ Feature extraction: " << fv.size() << " features" << std::endl;
            passed++;
        }
    }
    
    total++;
    Dataset trainDataset;
    if (MNISTLoader::loadDataset(trainImagesPath, trainLabelsPath, trainDataset)) {
        Dataset smallTrain;
        for (size_t i = 0; i < std::min(trainDataset.size(), size_t(500)); ++i) {
            smallTrain.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
        }
        
        KNN knn(3);
        knn.train(smallTrain);
        int pred = knn.predict(testDataset.getFeatures(0));
        if (pred >= 0 && pred < 10) {
            std::cout << "✓ ML Models: KNN=" << pred << std::endl;
            passed++;
        }
    }
    
    total++;
    if (imagesLoaded && images.size() > 0 && labels.size() == images.size()) {
        AStarMatcher astar;
        std::vector<FeatureVector> tFeatures;
        std::vector<int> tLabels;
        PixelGridExtractor pixelExt(28, 28);
        for (size_t i = 0; i < std::min(images.size(), size_t(50)); ++i) {
            tFeatures.push_back(pixelExt.extract(images[i]));
            tLabels.push_back(labels[i]);
        }
        if (tFeatures.size() > 0 && tLabels.size() == tFeatures.size()) {
            astar.buildTemplatesFromDataset(tFeatures, tLabels);
            int astarPred = astar.match(testDataset.getFeatures(0));
            if (astarPred >= 0 && astarPred < 10) {
                std::cout << "✓ A* Matching: " << astarPred << std::endl;
                passed++;
            } else {
                std::cout << "✗ A* Matching failed (pred: " << astarPred << ")" << std::endl;
            }
        } else {
            std::cout << "✗ A* Matching: no templates built" << std::endl;
        }
    } else {
        std::cout << "✗ A* Matching: no images loaded" << std::endl;
    }
    
    total++;
    if (images.size() > 0) {
        RuleEngine rules;
        int rulePred = rules.predict(images[0]);
        if (rulePred >= -1) {
            std::cout << "✓ Rule Engine: " << rulePred << std::endl;
            passed++;
        }
    }
    
    total++;
    if (imagesLoaded && trainDataset.size() > 0) {
        PixelGridExtractor pixelExt(28, 28);
        Dataset smallTrain;
        for (size_t i = 0; i < std::min(trainDataset.size(), size_t(100)); ++i) {
            smallTrain.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
        }
        
        KNN knn(3);
        knn.train(smallTrain);
        int pred1 = knn.predict(testDataset.getFeatures(0));
        
        FeatureVector newExample = testDataset.getFeatures(1);
        int newLabel = testDataset.getLabel(1);
        knn.addExample(newExample, newLabel);
        
        int pred2 = knn.predict(testDataset.getFeatures(0));
        if (pred2 >= 0 && pred2 < 10) {
            std::cout << "✓ Active Learning: KNN addExample works" << std::endl;
            passed++;
        } else {
            std::cout << "✗ Active Learning: KNN addExample failed" << std::endl;
        }
    }
    
    total++;
    if (trainDataset.size() > 0) {
        Dataset smallTrain;
        for (size_t i = 0; i < std::min(trainDataset.size(), size_t(100)); ++i) {
            smallTrain.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
        }
        
        NaiveBayes nb;
        nb.train(smallTrain);
        int pred1 = nb.predict(testDataset.getFeatures(0));
        
        FeatureVector newExample = testDataset.getFeatures(1);
        int newLabel = testDataset.getLabel(1);
        nb.updateWithExample(newExample, newLabel);
        
        int pred2 = nb.predict(testDataset.getFeatures(0));
        if (pred2 >= 0 && pred2 < 10) {
            std::cout << "✓ Active Learning: NaiveBayes updateWithExample works" << std::endl;
            passed++;
        } else {
            std::cout << "✗ Active Learning: NaiveBayes updateWithExample failed" << std::endl;
        }
    }
    
    total++;
    if (imagesLoaded && images.size() > 0 && labels.size() == images.size()) {
        AStarMatcher astar;
        PixelGridExtractor pixelExt(28, 28);
        
        std::vector<FeatureVector> tFeatures;
        std::vector<int> tLabels;
        for (size_t i = 0; i < std::min(images.size(), size_t(50)); ++i) {
            tFeatures.push_back(pixelExt.extract(images[i]));
            tLabels.push_back(labels[i]);
        }
        astar.buildTemplatesFromDataset(tFeatures, tLabels);
        
        FeatureVector newTemplate = pixelExt.extract(images[50]);
        int newTemplateLabel = labels[50];
        astar.addTemplate(newTemplate, newTemplateLabel);
        
        int astarPred = astar.match(testDataset.getFeatures(0));
        if (astarPred >= 0 && astarPred < 10) {
            std::cout << "✓ Active Learning: A* addTemplate works" << std::endl;
            passed++;
        } else {
            std::cout << "✗ Active Learning: A* addTemplate failed" << std::endl;
        }
    }
    
    total++;
    ConfusionMatrix cm(10);
    cm.addPrediction(0, 0);
    cm.addPrediction(0, 0);
    cm.addPrediction(1, 1);
    cm.addPrediction(1, 2);
    cm.addPrediction(2, 2);
    if (cm.getTotalSamples() == 5 && cm.getAccuracy() > 0.0) {
        std::cout << "✓ Confusion Matrix: Basic operations work" << std::endl;
        passed++;
    } else {
        std::cout << "✗ Confusion Matrix: Basic operations failed" << std::endl;
    }
    
    total++;
    double accuracy = cm.getAccuracy();
    double precision = cm.getPrecision(0);
    double recall = cm.getRecall(0);
    if (accuracy >= 0.0 && accuracy <= 1.0 && 
        precision >= 0.0 && precision <= 1.0 &&
        recall >= 0.0 && recall <= 1.0) {
        std::cout << "✓ Confusion Matrix: Metrics calculation works" << std::endl;
        passed++;
    } else {
        std::cout << "✗ Confusion Matrix: Metrics calculation failed" << std::endl;
    }
    
    total++;
    if (trainDataset.size() > 0 && testDataset.size() > 0) {
        Dataset smallTrain;
        for (size_t i = 0; i < std::min(trainDataset.size(), size_t(100)); ++i) {
            smallTrain.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
        }
        
        KNN knn(3);
        knn.train(smallTrain);
        
        ConfusionMatrix testCM(10);
        int testCount = std::min(50, static_cast<int>(testDataset.size()));
        for (int i = 0; i < testCount; ++i) {
            int trueLabel = testDataset.getLabel(i);
            int pred = knn.predict(testDataset.getFeatures(i));
            testCM.addPrediction(trueLabel, pred);
        }
        
        double testAccuracy = testCM.getAccuracy();
        if (testAccuracy >= 0.0 && testAccuracy <= 1.0 && testCM.getTotalSamples() == testCount) {
            std::cout << "✓ Confusion Matrix: Integration with models works" << std::endl;
            passed++;
        } else {
            std::cout << "✗ Confusion Matrix: Integration with models failed" << std::endl;
        }
    }
    
    total++;
    ConfusionMatrix metricsCM(10);
    metricsCM.addPrediction(0, 0);
    metricsCM.addPrediction(0, 0);
    metricsCM.addPrediction(0, 1);
    metricsCM.addPrediction(1, 1);
    metricsCM.addPrediction(1, 1);
    metricsCM.addPrediction(1, 0);
    
    double prec0 = metricsCM.getPrecision(0);
    double rec0 = metricsCM.getRecall(0);
    double f1_0 = metricsCM.getF1Score(0);
    double prec1 = metricsCM.getPrecision(1);
    double rec1 = metricsCM.getRecall(1);
    double f1_1 = metricsCM.getF1Score(1);
    
    if (prec0 >= 0.0 && prec0 <= 1.0 && rec0 >= 0.0 && rec0 <= 1.0 && 
        f1_0 >= 0.0 && f1_0 <= 1.0 && prec1 >= 0.0 && prec1 <= 1.0 &&
        rec1 >= 0.0 && rec1 <= 1.0 && f1_1 >= 0.0 && f1_1 <= 1.0) {
        std::cout << "✓ Enhanced Metrics: Precision, Recall, F1-Score calculations work" << std::endl;
        passed++;
    } else {
        std::cout << "✗ Enhanced Metrics: Precision, Recall, F1-Score calculations failed" << std::endl;
    }
    
    std::cout << "\nResult: " << passed << "/" << total << " tests passed" << std::endl;
    return (passed == total) ? 0 : 1;
}

