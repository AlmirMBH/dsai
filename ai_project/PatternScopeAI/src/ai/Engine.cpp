#include "Engine.h"
#include "features/PixelGridExtractor.h"
#include "core/ResourcePath.h"
#include <fstream>
#include <map>

void Engine::loadModels(Mode mode) {
    if (currentMode == mode) {
        return;
    }
    currentMode = mode;
    performanceStats.clear();

    std::string modeDirectory = ResourcePath::getModelsDir() + std::string(mode == Mode::DIGITS ? "digits" : (mode == Mode::SHAPES ? "shapes" : "symbols"));

    std::string knnPath = modeDirectory + "/knn.txt";
    std::ifstream knnFile(knnPath);
    if (knnFile) knn.load(knnFile);

    std::ifstream naiveBayesFile(modeDirectory + "/nb.txt");
    if (naiveBayesFile) naiveBayes.load(naiveBayesFile);

    int numClasses = (mode == Mode::DIGITS ? 10 : 3);
    mlp = MiniMLP(784, 64, numClasses);
    std::ifstream mlpFile(modeDirectory + "/mlp.txt");
    if (mlpFile) mlp.load(mlpFile);

    std::ifstream astarFile(modeDirectory + "/astar.txt");
    if (astarFile) astar.load(astarFile);
}

PredictionResult Engine::predict(Mode mode, const Image& image) {
    loadModels(mode);
    
    PixelGridExtractor extractor(28, 28); 
    auto features = extractor.extract(image);
    
    PredictionResult result;
    
    int knnLabel = knn.predict(features);
    double knnConf = knn.getConfidence(features);
    result.modelComparison["KNN"] = {knnLabel, knnConf};
    
    int nbLabel = naiveBayes.predict(features);
    double nbConf = naiveBayes.getConfidence(features);
    result.modelComparison["NaiveBayes"] = {nbLabel, nbConf};
    
    int mlpLabel = mlp.predict(features);
    double mlpConf = mlp.getConfidence(features);
    result.modelComparison["MiniMLP"] = {mlpLabel, mlpConf};
    
    int astarLabel = astar.match(features);
    double astarConf = astar.getConfidence(features);
    result.modelComparison["AStar"] = {astarLabel, astarConf};

    int ruleLabel = rules.predict(image);
    double ruleConf = rules.getConfidence(image);
    result.modelComparison["RuleEngine"] = {ruleLabel, ruleConf};

    std::map<int, double> classScores;
    classScores[knnLabel] += knnConf;
    classScores[nbLabel] += nbConf;
    classScores[mlpLabel] += mlpConf;
    classScores[astarLabel] += astarConf;

    int bestLabel = -1;
    double maxScore = -1.0;
    for (auto const& classScoreEntry : classScores) {
        if (classScoreEntry.second > maxScore) {
            maxScore = classScoreEntry.second;
            bestLabel = classScoreEntry.first;
        }
    }

    result.finalLabel = bestLabel;
    result.finalConfidence = maxScore / 4.0;
    result.finalModelName = "Hybrid Ensemble";

    return result;
}

void Engine::updateModel(Mode mode, const Image& image, int correctLabel) {
    loadModels(mode);
    PixelGridExtractor extractor(28, 28); 
    auto features = extractor.extract(image);
    
    knn.addExample(features, correctLabel);
    naiveBayes.addExample(features, correctLabel);
    mlp.addExample(features, correctLabel);
}

std::shared_ptr<ConfusionMatrix> Engine::getMetrics(Mode mode, const std::string& modelName) {
    loadModels(mode);
    
    if (performanceStats.count(modelName)) {
        return performanceStats[modelName];
    }
    
    std::string modeDirectory = ResourcePath::getModelsDir() + std::string(mode == Mode::DIGITS ? "digits" : (mode == Mode::SHAPES ? "shapes" : "symbols"));
    std::string statsFile = modeDirectory + "/" + (modelName == "KNN" ? "knn_stats.txt" : 
                                            (modelName == "NaiveBayes" ? "nb_stats.txt" : 
                                            (modelName == "MiniMLP" ? "mlp_stats.txt" : "astar_stats.txt")));
    
    auto matrix = std::make_shared<ConfusionMatrix>();
    std::ifstream inputStream(statsFile);
    if (inputStream) { 
        matrix->load(inputStream); 
        performanceStats[modelName] = matrix; 
        return matrix; 
    }
    return nullptr;
}
