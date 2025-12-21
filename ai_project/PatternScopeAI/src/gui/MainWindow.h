#pragma once
#include <gui/Window.h>
#include "StartView.h"
#include "MainView.h"

/**
 * Main application window that handles switching between 
 * the startup mode-selection view and the main interactive view.
 */
class MainWindow : public gui::Window
{
protected:
    StartView startView;
    MainView mainView;

public:
    MainWindow()
    : gui::Window(gui::Geometry(100, 100, 1200, 800))
    {
        setTitle("PatternVision++");
        // Show the selection screen first.
        setCentralView(&startView);
    }

    /**
     * Handle transitions between screens.
     */
    bool onClick(gui::Button* pBtn) override
    {
        // When the user clicks the start button on the first screen:
        if (pBtn == startView.getStartButton()) {
            // Apply the chosen mode to the main view and switch to it.
            mainView.setMode(startView.getSelectedMode());
            setCentralView(&mainView);
            return true;
        }
        return false;
    }
};
