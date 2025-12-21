#pragma once
#include <gui/View.h>
#include <gui/Button.h>
#include <gui/Label.h>
#include "DrawingCanvas.h"
#include "../ai/Engine.h"

class MainView : public gui::View
{
protected:
    Engine engine;
    Mode currentMode = Mode::DIGITS;

    DrawingCanvas canvas;
    
    // Prediction Panel
    gui::Label lblPredictionTitle;
    gui::Label lblTopClass;
    gui::Label lblConfidence;
    gui::Label lblAgentWarning;

    // Model Comparison
    gui::Label lblComparisonTitle;
    gui::Label lblKNN;
    gui::Label lblNaiveBayes;
    gui::Label lblMLP;

    // A* & Rules
    gui::Label lblAStarRulesTitle;
    gui::Label lblAStarMatch;
    gui::Label lblRuleReason;

    // Footer Buttons
    gui::Button btnLoadImage;
    gui::Button btnPredict;
    gui::Button btnClear;
    gui::Button btnTrain;
    gui::Button btnConfusionMatrix;
    
    // Active Learning Feedback
    gui::Label lblFeedback;
    gui::Button btnCorrect;
    gui::Button btnWrong;

    void updateUI(const PredictionResult& result);

public:
    MainView();
    void setMode(Mode mode);
    bool onClick(gui::Button* pBtn) override;
    bool handleUserEvent(td::UINT4 eventID, const td::Variant& userParam) override;
    
    // Triggered when drawing changes
    void processDrawing();
};
