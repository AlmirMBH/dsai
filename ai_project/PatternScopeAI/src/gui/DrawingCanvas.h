#pragma once
#include <gui/Canvas.h>
#include <gui/Shape.h>
#include <td/ColorID.h>
#include <td/Point.h>
#include <vector>
#include <string>
#include "../data/Image.h"
#include "../data/Dataset.h"
#include "../data/FeatureVector.h"
#include "../data/MNISTLoader.h"
#include "../ai/features/PixelGridExtractor.h"
#include "../ai/models/KNN.h"
#include "../ai/models/NaiveBayes.h"
#include "../ai/models/MiniMLP.h"
#include "../ai/search/AStarMatcher.h"
#include "../ai/rules/RuleEngine.h"

class DrawingCanvas : public gui::Canvas {
protected:
    std::vector<std::vector<bool>> pixels;
    int canvasWidth;
    int canvasHeight;
    int imageSize;
    
    KNN knn;
    NaiveBayes nb;
    MiniMLP mlp;
    AStarMatcher astar;
    RuleEngine rules;
    PixelGridExtractor featureExtractor;
    bool modelsTrained;
    
    int knnPred;
    int nbPred;
    int mlpPred;
    int astarPred;
    int rulePred;
    double knnConf;
    double nbConf;
    double mlpConf;
    double astarConf;
    double ruleConf;
    
    double confidenceThreshold;
    bool activeLearningEnabled;
    
    void onResize(const gui::Size& newSize) override;
    void onDraw(const gui::Rect& rect) override;
    void onMouseDown(const gui::Point& point) override;
    void onMouseMove(const gui::Point& point) override;
    
    Image getImageFromCanvas();
    void drawPredictions();
    void trainModels();
    bool isLowConfidence() const;
    void updateModelsWithExample(const FeatureVector& features, int label);

public:
    DrawingCanvas();
    void clear();
    void updatePredictions();
    
    int getKNNPrediction() const { return knnPred; }
    int getNBPrediction() const { return nbPred; }
    int getMLPPrediction() const { return mlpPred; }
    int getAStarPrediction() const { return astarPred; }
    int getRulePrediction() const { return rulePred; }
    
    double getKNNConfidence() const { return knnConf; }
    double getNBConfidence() const { return nbConf; }
    double getMLPConfidence() const { return mlpConf; }
    double getAStarConfidence() const { return astarConf; }
    double getRuleConfidence() const { return ruleConf; }
    
    bool areModelsTrained() const { return modelsTrained; }
    bool isActiveLearningEnabled() const { return activeLearningEnabled; }
    void setActiveLearningEnabled(bool enabled) { activeLearningEnabled = enabled; }
    void setConfidenceThreshold(double threshold) { confidenceThreshold = threshold; }
    double getConfidenceThreshold() const { return confidenceThreshold; }
    FeatureVector getCurrentFeatures() const;
};

