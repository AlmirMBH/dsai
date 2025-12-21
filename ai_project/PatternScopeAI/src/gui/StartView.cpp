#include "StartView.h"
#include <gui/VerticalLayout.h>
#include <gui/HorizontalLayout.h>

/**
 * Initialize the startup view with mode selection buttons.
 */
StartView::StartView()
: titleLabel("PatternVision++"),
  subtitleLabel("Choose recognition mode"),
  btnDigits("Digits (0-9)"),
  btnShapes("Geometric Shapes"),
  btnSymbols("Custom Symbols"),
  btnStart("Start Application")
{
    gui::VerticalLayout mainLayout(6);
    mainLayout.setMargins(100, 100);

    // Add labels and buttons to the vertical stack.
    mainLayout.append(titleLabel);
    mainLayout.append(subtitleLabel);
    
    mainLayout.append(btnDigits);
    mainLayout.append(btnShapes);
    mainLayout.append(btnSymbols);
    
    mainLayout.append(btnStart);

    setLayout(&mainLayout);
}

/**
 * Handle button clicks to select the recognition mode.
 */
bool StartView::onClick(gui::Button* pBtn) {
    if (pBtn == &btnDigits) {
        selectedMode = Mode::DIGITS;
        return true;
    }
    if (pBtn == &btnShapes) {
        selectedMode = Mode::SHAPES;
        return true;
    }
    if (pBtn == &btnSymbols) {
        selectedMode = Mode::SYMBOLS;
        return true;
    }
    // "Start" button click is handled by the MainWindow.
    return false;
}
