#include "MainView.h"
#include <gui/HorizontalLayout.h>
#include <gui/VerticalLayout.h>
#include <sstream>
#include <iomanip>
#include <iostream>

MainView::MainView() : btnClear("Clear"), btnPredict("Predict"),
    lblKNN("KNN: -"), lblNB("NB: -"), lblMLP("MLP: -"),
    lblAStar("A*: -"), lblRule("Rule: -") {
    gui::HorizontalLayout hLayout(2);
    gui::VerticalLayout leftLayout(7);
    
    leftLayout.append(btnClear);
    leftLayout.append(btnPredict);
    leftLayout.append(lblKNN);
    leftLayout.append(lblNB);
    leftLayout.append(lblMLP);
    leftLayout.append(lblAStar);
    leftLayout.append(lblRule);
    
    hLayout.append(leftLayout);
    hLayout.append(canvas);
    
    setLayout(&hLayout);
}

bool MainView::onClick(gui::Button* pBtn) {
    if (pBtn == &btnClear) {
        canvas.clear();
        return true;
    }
    
    if (pBtn == &btnPredict) {
        updatePredictions();
        return true;
    }
    
    return false;
}

void MainView::updatePredictions() {
    canvas.updatePredictions();
    updatePredictionDisplay();
    
    if (canvas.isActiveLearningEnabled() && canvas.isLowConfidence()) {
        handleActiveLearning();
    }
}

void MainView::handleActiveLearning() {
    std::cout << "\nLow confidence prediction detected." << std::endl;
    std::cout << "Enter correct label (0-9) or -1 to skip: ";
    
    int correctLabel;
    std::cin >> correctLabel;
    
    if (correctLabel >= 0 && correctLabel < 10) {
        FeatureVector features = canvas.getCurrentFeatures();
        canvas.updateModelsWithExample(features, correctLabel);
        std::cout << "Model updated with label: " << correctLabel << std::endl;
        
        canvas.updatePredictions();
        updatePredictionDisplay();
    }
}

void MainView::updatePredictionDisplay() {
    if (!canvas.areModelsTrained()) {
        return;
    }
    
    std::ostringstream oss;
    
    oss << "KNN: " << canvas.getKNNPrediction() 
        << " (" << std::fixed << std::setprecision(2) << canvas.getKNNConfidence() << ")";
    lblKNN.setText(oss.str().c_str());
    
    oss.str("");
    oss << "NB: " << canvas.getNBPrediction() 
        << " (" << std::fixed << std::setprecision(2) << canvas.getNBConfidence() << ")";
    lblNB.setText(oss.str().c_str());
    
    oss.str("");
    oss << "MLP: " << canvas.getMLPPrediction() 
        << " (" << std::fixed << std::setprecision(2) << canvas.getMLPConfidence() << ")";
    lblMLP.setText(oss.str().c_str());
    
    oss.str("");
    oss << "A*: " << canvas.getAStarPrediction() 
        << " (" << std::fixed << std::setprecision(2) << canvas.getAStarConfidence() << ")";
    lblAStar.setText(oss.str().c_str());
    
    oss.str("");
    oss << "Rule: " << canvas.getRulePrediction() 
        << " (" << std::fixed << std::setprecision(2) << canvas.getRuleConfidence() << ")";
    lblRule.setText(oss.str().c_str());
}

