#include "MainView.h"
#include <gui/HorizontalLayout.h>
#include <gui/VerticalLayout.h>

MainView::MainView() : btnClear("Clear"), btnPredict("Predict") {
    gui::HorizontalLayout hLayout(2);
    gui::VerticalLayout buttonLayout(2);
    
    buttonLayout.append(btnClear);
    buttonLayout.append(btnPredict);
    
    hLayout.append(buttonLayout);
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
}

