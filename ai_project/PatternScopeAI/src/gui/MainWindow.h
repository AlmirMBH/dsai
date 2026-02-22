#pragma once
#include <gui/Window.h>
#include "MainView.h"

class MainWindow : public gui::Window
{
protected:
    MainView mainView;
    bool onClick(gui::Button* button) override { return mainView.onClick(button); }

public:
    MainWindow() : gui::Window(gui::Size(1200, 800)) {
        setTitle("PatternVision++");
        setCentralView(&mainView, gui::Frame::FixSizes::No);
    }
};
