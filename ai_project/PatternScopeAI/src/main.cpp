#include <iostream>
#include <iomanip>
#include <string>
#include "data/Image.h"
#include "data/FeatureVector.h"
#include "data/Dataset.h"
#include "data/MNISTLoader.h"
#include "data/ConfusionMatrix.h"
#include "ai/features/FeatureExtractor.h"
#include "ai/features/PixelGridExtractor.h"
#include "ai/features/EdgeMapExtractor.h"
#include "ai/features/HOGExtractor.h"
#include "ai/models/Model.h"
#include "ai/models/KNN.h"
#include "ai/models/NaiveBayes.h"
#include "ai/models/MiniMLP.h"
#include "ai/search/AStarMatcher.h"
#include "ai/rules/RuleEngine.h"
#include "ai/rules/StructuralFeatures.h"

int main(int argc, const char* argv[]) {
    std::cout << "PatternScope AI - Console Test Harness" << std::endl;
    std::cout << "=======================================" << std::endl;
    
    Dataset trainDataset;
    Dataset testDataset;
    
    std::string trainImagesPath = "../mnist/train-images.idx3-ubyte";
    std::string trainLabelsPath = "../mnist/train-labels.idx1-ubyte";
    std::string testImagesPath = "../mnist/t10k-images.idx3-ubyte";
    std::string testLabelsPath = "../mnist/t10k-labels.idx1-ubyte";
    
    std::cout << "Loading training dataset..." << std::endl;
    if (!MNISTLoader::loadDataset(trainImagesPath, trainLabelsPath, trainDataset)) {
        std::cout << "Failed to load training dataset!" << std::endl;
        return 1;
    }
    std::cout << "Loaded " << trainDataset.size() << " training samples" << std::endl;
    
    std::cout << "Loading test dataset..." << std::endl;
    if (!MNISTLoader::loadDataset(testImagesPath, testLabelsPath, testDataset)) {
        std::cout << "Failed to load test dataset!" << std::endl;
        return 1;
    }
    std::cout << "Loaded " << testDataset.size() << " test samples" << std::endl;
    
    if (testDataset.size() > 0) {
        std::cout << "\nFirst test sample:" << std::endl;
        std::cout << "Label: " << testDataset.getLabel(0) << std::endl;
        std::cout << "Features: " << testDataset.getFeatures(0).size() << " dimensions" << std::endl;
        
        std::cout << "\nTesting feature extractors..." << std::endl;
        
        std::vector<Image> images;
        std::vector<int> labels;
        if (MNISTLoader::loadImages(testImagesPath, images) && 
            MNISTLoader::loadLabels(testLabelsPath, labels) && 
            images.size() > 0) {
            
            Image sampleImage = images[0];
            
            PixelGridExtractor pixelExtractor(28, 28);
            FeatureVector pixelFeatures = pixelExtractor.extract(sampleImage);
            std::cout << "PixelGrid: " << pixelFeatures.size() << " features" << std::endl;
            
            EdgeMapExtractor edgeExtractor(28, 28);
            FeatureVector edgeFeatures = edgeExtractor.extract(sampleImage);
            std::cout << "EdgeMap: " << edgeFeatures.size() << " features" << std::endl;
            
            HOGExtractor hogExtractor(8, 2, 9);
            FeatureVector hogFeatures = hogExtractor.extract(sampleImage);
            std::cout << "HOG: " << hogFeatures.size() << " features" << std::endl;
        }
    }
    
    std::cout << "\nFeature extraction complete. Ready for ML models." << std::endl;
    
    std::cout << "\n=== Training ML Models ===" << std::endl;
    
    Dataset smallTrainDataset;
    for (size_t i = 0; i < std::min(trainDataset.size(), size_t(1000)); ++i) {
        smallTrainDataset.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
    }
    std::cout << "Using " << smallTrainDataset.size() << " samples for training" << std::endl;
    
    std::cout << "\nTraining KNN..." << std::endl;
    KNN knn(3);
    knn.train(smallTrainDataset);
    std::cout << "KNN training complete." << std::endl;
    
    std::cout << "\nTraining NaiveBayes..." << std::endl;
    NaiveBayes nb;
    nb.train(smallTrainDataset);
    std::cout << "NaiveBayes training complete." << std::endl;
    
    std::cout << "\nTraining MiniMLP..." << std::endl;
    MiniMLP mlp(784, 64, 10);
    mlp.train(smallTrainDataset);
    std::cout << "MiniMLP training complete." << std::endl;
    
    std::cout << "\n=== Testing ML Models ===" << std::endl;
    
    int testCount = std::min(100, static_cast<int>(testDataset.size()));
    int knnCorrect = 0, nbCorrect = 0, mlpCorrect = 0;
    
    ConfusionMatrix knnCM(10);
    ConfusionMatrix nbCM(10);
    ConfusionMatrix mlpCM(10);
    
    for (int i = 0; i < testCount; ++i) {
        const FeatureVector& features = testDataset.getFeatures(i);
        int trueLabel = testDataset.getLabel(i);
        
        int knnPred = knn.predict(features);
        int nbPred = nb.predict(features);
        int mlpPred = mlp.predict(features);
        
        if (knnPred == trueLabel) knnCorrect++;
        if (nbPred == trueLabel) nbCorrect++;
        if (mlpPred == trueLabel) mlpCorrect++;
        
        knnCM.addPrediction(trueLabel, knnPred);
        nbCM.addPrediction(trueLabel, nbPred);
        mlpCM.addPrediction(trueLabel, mlpPred);
    }
    
    std::cout << "\nResults on " << testCount << " test samples:" << std::endl;
    std::cout << "KNN: " << knnCorrect << "/" << testCount << " (" 
              << (100.0 * knnCorrect / testCount) << "%)" << std::endl;
    std::cout << "NaiveBayes: " << nbCorrect << "/" << testCount << " (" 
              << (100.0 * nbCorrect / testCount) << "%)" << std::endl;
    std::cout << "MiniMLP: " << mlpCorrect << "/" << testCount << " (" 
              << (100.0 * mlpCorrect / testCount) << "%)" << std::endl;
    
    std::cout << "\n=== Confusion Matrices ===" << std::endl;
    
    std::cout << "\nKNN Confusion Matrix:" << std::endl;
    knnCM.print(std::cout);
    std::cout << "Accuracy: " << (100.0 * knnCM.getAccuracy()) << "%" << std::endl;
    std::cout << "\nPer-class metrics:" << std::endl;
    std::cout << "Class | Precision | Recall | F1-Score" << std::endl;
    std::cout << "------|-----------|--------|---------" << std::endl;
    for (int c = 0; c < 10; ++c) {
        std::cout << std::setw(5) << c << " | " 
                  << std::fixed << std::setprecision(3) << std::setw(9) << knnCM.getPrecision(c) << " | "
                  << std::setw(6) << knnCM.getRecall(c) << " | "
                  << std::setw(8) << knnCM.getF1Score(c) << std::endl;
    }
    
    std::cout << "\nNaiveBayes Confusion Matrix:" << std::endl;
    nbCM.print(std::cout);
    std::cout << "Accuracy: " << (100.0 * nbCM.getAccuracy()) << "%" << std::endl;
    std::cout << "\nPer-class metrics:" << std::endl;
    std::cout << "Class | Precision | Recall | F1-Score" << std::endl;
    std::cout << "------|-----------|--------|---------" << std::endl;
    for (int c = 0; c < 10; ++c) {
        std::cout << std::setw(5) << c << " | " 
                  << std::fixed << std::setprecision(3) << std::setw(9) << nbCM.getPrecision(c) << " | "
                  << std::setw(6) << nbCM.getRecall(c) << " | "
                  << std::setw(8) << nbCM.getF1Score(c) << std::endl;
    }
    
    std::cout << "\nMiniMLP Confusion Matrix:" << std::endl;
    mlpCM.print(std::cout);
    std::cout << "Accuracy: " << (100.0 * mlpCM.getAccuracy()) << "%" << std::endl;
    std::cout << "\nPer-class metrics:" << std::endl;
    std::cout << "Class | Precision | Recall | F1-Score" << std::endl;
    std::cout << "------|-----------|--------|---------" << std::endl;
    for (int c = 0; c < 10; ++c) {
        std::cout << std::setw(5) << c << " | " 
                  << std::fixed << std::setprecision(3) << std::setw(9) << mlpCM.getPrecision(c) << " | "
                  << std::setw(6) << mlpCM.getRecall(c) << " | "
                  << std::setw(8) << mlpCM.getF1Score(c) << std::endl;
    }
    
    if (testDataset.size() > 0) {
        std::cout << "\nSample prediction (first test sample):" << std::endl;
        std::cout << "True label: " << testDataset.getLabel(0) << std::endl;
        const FeatureVector& features = testDataset.getFeatures(0);
        std::cout << "KNN prediction: " << knn.predict(features) 
                  << " (confidence: " << knn.getConfidence(features) << ")" << std::endl;
        std::cout << "NaiveBayes prediction: " << nb.predict(features) 
                  << " (confidence: " << nb.getConfidence(features) << ")" << std::endl;
        std::cout << "MiniMLP prediction: " << mlp.predict(features) 
                  << " (confidence: " << mlp.getConfidence(features) << ")" << std::endl;
    }
    
    std::cout << "\n=== Phase 4: A* Template Matching ===" << std::endl;
    
    std::vector<Image> images;
    std::vector<int> labels;
    if (MNISTLoader::loadImages(testImagesPath, images) && 
        MNISTLoader::loadLabels(testLabelsPath, labels)) {
        
        PixelGridExtractor pixelExtractor(28, 28);
        std::vector<FeatureVector> templateFeatures;
        std::vector<int> templateLabels;
        
        for (size_t i = 0; i < std::min(images.size(), size_t(100)); ++i) {
            templateFeatures.push_back(pixelExtractor.extract(images[i]));
            templateLabels.push_back(labels[i]);
        }
        
        AStarMatcher astarMatcher;
        astarMatcher.buildTemplatesFromDataset(templateFeatures, templateLabels);
        std::cout << "Built " << templateFeatures.size() << " templates" << std::endl;
        
        if (testDataset.size() > 0) {
            const FeatureVector& query = testDataset.getFeatures(0);
            int astarPred = astarMatcher.match(query);
            double astarConf = astarMatcher.getConfidence(query);
            std::cout << "A* prediction: " << astarPred 
                      << " (confidence: " << astarConf << ")" << std::endl;
        }
    }
    
    std::cout << "\n=== Phase 5: Rule-Based Reasoning ===" << std::endl;
    
    RuleEngine ruleEngine;
    std::vector<Image> testImages;
    std::vector<int> testLabels;
    if (MNISTLoader::loadImages(testImagesPath, testImages) && 
        MNISTLoader::loadLabels(testLabelsPath, testLabels) && 
        testImages.size() > 0) {
        
        std::cout << "Testing structural features..." << std::endl;
        Image sampleImage = testImages[0];
        std::vector<double> structFeatures = StructuralFeatures::extractAll(sampleImage);
        std::cout << "Edges: " << structFeatures[0] 
                  << ", Corners: " << structFeatures[1]
                  << ", Aspect Ratio: " << structFeatures[2]
                  << ", Symmetry: " << structFeatures[3] << std::endl;
        
        int rulePred = ruleEngine.predict(sampleImage);
        double ruleConf = ruleEngine.getConfidence(sampleImage);
        std::cout << "Rule-based prediction: " << rulePred 
                  << " (confidence: " << ruleConf << ")" << std::endl;
    }
    
    std::cout << "\n=== All Components Complete ===" << std::endl;
    std::cout << "Phases 1-5 implemented and tested!" << std::endl;
    
    return 0;
}

