#pragma once
#include <gui/Canvas.h>
#include "../data/Image.h"

class DrawingCanvas : public gui::Canvas
{
protected:
    Image canvasImage;
    bool isDrawing = false;
    int brushSize = 2;

public:
    DrawingCanvas();
    void onDraw(const gui::Rect& rect) override;
    void onPrimaryButtonPressed(const gui::InputDevice& inputDevice) override;
    void onPrimaryButtonReleased(const gui::InputDevice& inputDevice) override;
    void onCursorDragged(const gui::InputDevice& inputDevice) override;

    void clear();
    const Image& getImage() const { return canvasImage; }
    
    // Resize the drawing to 28x28 for the engine
    Image getResizedImage() const;
};
