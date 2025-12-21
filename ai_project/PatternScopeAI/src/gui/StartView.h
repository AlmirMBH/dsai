#pragma once
#include <gui/View.h>
#include <gui/Button.h>
#include <gui/Label.h>
#include "../data/Mode.h"

class StartView : public gui::View
{
protected:
    gui::Label titleLabel;
    gui::Label subtitleLabel;
    gui::Button btnDigits;
    gui::Button btnShapes;
    gui::Button btnSymbols;
    gui::Button btnStart;

    Mode selectedMode = Mode::DIGITS;

    void updateSelection();

public:
    StartView();
    bool onClick(gui::Button* pBtn) override;
    Mode getSelectedMode() const { return selectedMode; }
    gui::Button* getStartButton() { return &btnStart; }
};

