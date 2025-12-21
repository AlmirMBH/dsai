#pragma once
#include "../data/Image.h"
#include "../data/Mode.h"
#include "models/KNN.h"
#include "models/NaiveBayes.h"
#include "models/MiniMLP.h"
#include "search/AStarMatcher.h"
#include "rules/RuleEngine.h"
#include "../data/ConfusionMatrix.h"
#include <string>
#include <memory>
#include <map>

struct ModelResult {
    int label;
    double confidence;
};

struct PredictionResult { 
    int finalLabel; 
    double finalConfidence; 
    std::string finalModelName; 
    std::map<std::string, ModelResult> modelComparison;
};

class Engine {
    Mode currentMode;
    KNN knn; 
    NaiveBayes naiveBayes; 
    MiniMLP mlp; 
    AStarMatcher astar; 
    RuleEngine rules;
    std::map<std::string, std::shared_ptr<ConfusionMatrix>> performanceStats;
    
    void loadModels(Mode mode);

public:
    Engine() : currentMode((Mode)-1) {}

    PredictionResult predict(Mode mode, const Image& image);
    void updateModel(Mode mode, const Image& image, int correctLabel);
    std::shared_ptr<ConfusionMatrix> getMetrics(Mode mode, const std::string& modelName);
};
