#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include "data/DataManager.h"
#include "data/ConfusionMatrix.h"
#include "ai/models/KNN.h"
#include "ai/models/NaiveBayes.h"
#include "ai/models/MiniMLP.h"
#include "ai/search/AStarMatcher.h"

/**
 * Train every model using the training dataset and 
 * save their internal logic to text files. Test the 
 * models using the test dataset and save the performance 
 * results to separate stats files.
 */
void trainAndSave(const Dataset& trainingSet, const Dataset& testSet, std::string modeName, int numClasses) {
    std::cout << "Starting training process for: " << modeName << "..." << std::endl;
    
    mkdir("models", 0777); 
    mkdir(("models/" + modeName).c_str(), 0777);
    
    std::string modelDirectoryPath = "models/" + modeName + "/";

    KNN knnModel(3); 
    knnModel.train(trainingSet); 
    std::ofstream knnModelFile(modelDirectoryPath + "knn.txt"); 
    knnModel.save(knnModelFile);

    NaiveBayes naiveBayesModel; 
    naiveBayesModel.train(trainingSet); 
    std::ofstream naiveBayesModelFile(modelDirectoryPath + "nb.txt"); 
    naiveBayesModel.save(naiveBayesModelFile);

    MiniMLP miniMlpModel(784, 64, numClasses); 
    miniMlpModel.train(trainingSet); 
    std::ofstream miniMlpModelFile(modelDirectoryPath + "mlp.txt"); 
    miniMlpModel.save(miniMlpModelFile);

    AStarMatcher aStarMatcher; 
    std::vector<FeatureVector> templateFeatureVectors; 
    std::vector<int> templateLabelValues;
    int templateLimitCount = std::min((int)trainingSet.size(), 200);
    for (int sampleIndex = 0; sampleIndex < templateLimitCount; ++sampleIndex) {
        templateFeatureVectors.push_back(trainingSet.getFeatures(sampleIndex)); 
        templateLabelValues.push_back(trainingSet.getLabel(sampleIndex));
    }
    aStarMatcher.buildTemplatesFromDataset(templateFeatureVectors, templateLabelValues); 
    std::ofstream aStarMatcherFile(modelDirectoryPath + "astar.txt"); 
    aStarMatcher.save(aStarMatcherFile);

    ConfusionMatrix knnPerformanceMatrix(numClasses), naiveBayesPerformanceMatrix(numClasses), miniMlpPerformanceMatrix(numClasses), aStarPerformanceMatrix(numClasses);
    for (int sampleIndex = 0; sampleIndex < (int)testSet.size(); ++sampleIndex) { 
        auto featureVector = testSet.getFeatures(sampleIndex); 
        int trueLabelValue = testSet.getLabel(sampleIndex); 
        knnPerformanceMatrix.addPrediction(trueLabelValue, knnModel.predict(featureVector)); 
        naiveBayesPerformanceMatrix.addPrediction(trueLabelValue, naiveBayesModel.predict(featureVector)); 
        miniMlpPerformanceMatrix.addPrediction(trueLabelValue, miniMlpModel.predict(featureVector)); 
        aStarPerformanceMatrix.addPrediction(trueLabelValue, aStarMatcher.match(featureVector)); 
    }
    
    std::ofstream knnStatsFile(modelDirectoryPath + "knn_stats.txt"); 
    knnPerformanceMatrix.save(knnStatsFile);
    std::ofstream naiveBayesStatsFile(modelDirectoryPath + "nb_stats.txt"); 
    naiveBayesPerformanceMatrix.save(naiveBayesStatsFile);
    std::ofstream miniMlpStatsFile(modelDirectoryPath + "mlp_stats.txt"); 
    miniMlpPerformanceMatrix.save(miniMlpStatsFile);
    std::ofstream aStarStatsFile(modelDirectoryPath + "astar_stats.txt"); 
    aStarPerformanceMatrix.save(aStarStatsFile);

    std::cout << "✓ Training for " << modeName << " completed successfully." << std::endl;
}

/**
 * This is the entry point for the training tool. Load 
 * digits, shapes, and symbols datasets. 
 * Start the training and evaluation process for each mode.
 */
int main() {
    std::cout << "PatternScope: Initializing Model Training..." << std::endl;

    Dataset digitsTrainingDataset, digitsTestDataset;
    if (DataManager::loadMNIST("../mnist/train-images.idx3-ubyte", "../mnist/train-labels.idx1-ubyte", digitsTrainingDataset) &&
        DataManager::loadMNIST("../mnist/t10k-images.idx3-ubyte", "../mnist/t10k-labels.idx1-ubyte", digitsTestDataset)) {
        trainAndSave(digitsTrainingDataset, digitsTestDataset, "digits", 10);
    }
    
    Dataset shapesTrainingDataset, shapesTestDataset; 
    DataManager::loadShapes(shapesTrainingDataset, 1000); 
    DataManager::loadShapes(shapesTestDataset, 200); 
    trainAndSave(shapesTrainingDataset, shapesTestDataset, "shapes", 3);
    
    Dataset symbolsTrainingDataset, symbolsTestDataset; 
    DataManager::loadSymbols(symbolsTrainingDataset, 1000); 
    DataManager::loadSymbols(symbolsTestDataset, 200); 
    trainAndSave(symbolsTrainingDataset, symbolsTestDataset, "symbols", 3);
    
    std::cout << "All training tasks finished. Models are saved in the 'models/' directory." << std::endl;
    return 0;
}
