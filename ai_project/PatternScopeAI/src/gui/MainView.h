#pragma once
#include <gui/View.h>
#include <gui/Button.h>
#include "DrawingCanvas.h"
#include <vector>
#include <string>

class MainView : public gui::View {
protected:
    DrawingCanvas canvas;
    gui::Button btnClear;
    gui::Button btnPredict;
    gui::Button lblKNN;
    gui::Button lblNB;
    gui::Button lblMLP;
    gui::Button lblAStar;
    gui::Button lblRule;
    
    void updatePredictions();
    void updatePredictionDisplay();
    void handleActiveLearning();

public:
    MainView();
    bool onClick(gui::Button* pBtn) override;
};

