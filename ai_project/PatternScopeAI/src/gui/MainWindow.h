#pragma once
#include <gui/Window.h>
#include "MainView.h"

class MainWindow : public gui::Window {
protected:
    MainView view;

public:
    MainWindow()
    : gui::Window(gui::Geometry(50, 50, 1200, 800)) {
        setTitle("PatternScope AI");
        setCentralView(&view);
    }
};

