#include "DrawingCanvas.h"
#include <gui/Canvas.h>
#include <gui/Shape.h>
#include <algorithm>

DrawingCanvas::DrawingCanvas()
: canvasImage(280, 280) 
{
}

/**
 * Draw the canvas background and all white pixels that 
 * represent the user's drawing.
 */
void DrawingCanvas::onDraw(const gui::Rect& rect) {
    // Fill the background with black.
    gui::Shape background;
    background.createRect(rect);
    background.drawFill(td::ColorID::Black);

    // Draw every white pixel stored in our image object.
    for (int y = 0; y < canvasImage.getHeight(); ++y) {
        for (int x = 0; x < canvasImage.getWidth(); ++x) {
            if (canvasImage.getPixel(x, y) > 0) {
                gui::Shape pixel;
                pixel.createRect(gui::Rect(x, y, x + 1, y + 1));
                pixel.drawFill(td::ColorID::White);
            }
        }
    }
}

/**
 * Start drawing when the primary mouse button is pressed.
 */
void DrawingCanvas::onPrimaryButtonPressed(const gui::InputDevice& inputDevice) {
    isDrawing = true;
    onCursorDragged(inputDevice);
}

/**
 * Stop drawing when the mouse button is released.
 */
void DrawingCanvas::onPrimaryButtonReleased(const gui::InputDevice& inputDevice) {
    isDrawing = false;
    // Notify the parent view that the drawing has changed.
    if (getParentFrame()) {
        getParentFrame()->handleUserEvent(1); 
    }
}

/**
 * Add white pixels to the canvas as the user moves the mouse.
 */
void DrawingCanvas::onCursorDragged(const gui::InputDevice& inputDevice) {
    if (!isDrawing) {
        return;
    }

    const gui::Point& point = inputDevice.getFramePoint();
    int xCoordinate = (int)point.x;
    int yCoordinate = (int)point.y;

    // Draw a small square around the cursor to act as a brush.
    for (int dy = -brushSize; dy <= brushSize; ++dy) {
        for (int dx = -brushSize; dx <= brushSize; ++dx) {
            canvasImage.setPixel(xCoordinate + dx, yCoordinate + dy, 255);
        }
    }
    reDraw();
}

/**
 * Reset the canvas to all black pixels.
 */
void DrawingCanvas::clear() {
    for (int y = 0; y < canvasImage.getHeight(); ++y) {
        for (int x = 0; x < canvasImage.getWidth(); ++x) {
            canvasImage.setPixel(x, y, 0);
        }
    }
    reDraw();
}

/**
 * Scale the user drawing down to 28x28 for the AI models.
 */
Image DrawingCanvas::getResizedImage() const {
    Image resized(28, 28);
    int originalWidth = canvasImage.getWidth();
    int originalHeight = canvasImage.getHeight();
    
    for (int y = 0; y < 28; ++y) {
        for (int x = 0; x < 28; ++x) {
            int sourceX = (x * originalWidth) / 28;
            int sourceY = (y * originalHeight) / 28;
            resized.setPixel(x, y, canvasImage.getPixel(sourceX, sourceY));
        }
    }
    return resized;
}
