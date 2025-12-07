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
    
    void updatePredictions();

public:
    MainView();
    bool onClick(gui::Button* pBtn) override;
};

