#include "DrawingCanvas.h"
#include <algorithm>
#include <cmath>

DrawingCanvas::DrawingCanvas() : imageSize(28), modelsTrained(false) {
    enableResizeEvent(true);
    pixels.resize(imageSize, std::vector<bool>(imageSize, false));
    canvasWidth = 0;
    canvasHeight = 0;
}

void DrawingCanvas::onResize(const gui::Size& newSize) {
    canvasWidth = static_cast<int>(newSize.width);
    canvasHeight = static_cast<int>(newSize.height);
    reDraw();
}

void DrawingCanvas::onDraw(const gui::Rect& rect) {
    gui::Shape bg;
    gui::Rect bgRect(0, 0, canvasWidth, canvasHeight);
    bg.createRect(bgRect);
    bg.drawFill(td::ColorID::White);
    
    double cellWidth = static_cast<double>(canvasWidth) / imageSize;
    double cellHeight = static_cast<double>(canvasHeight) / imageSize;
    
    for (int y = 0; y < imageSize; ++y) {
        for (int x = 0; x < imageSize; ++x) {
            if (pixels[y][x]) {
                gui::Shape cell;
                gui::Rect cellRect(x * cellWidth, y * cellHeight, 
                                  (x + 1) * cellWidth, (y + 1) * cellHeight);
                cell.createRect(cellRect);
                cell.drawFill(td::ColorID::Black);
            }
        }
    }
    
    drawPredictions();
}

void DrawingCanvas::onMouseDown(const gui::Point& point) {
    int x = static_cast<int>((point.x / canvasWidth) * imageSize);
    int y = static_cast<int>((point.y / canvasHeight) * imageSize);
    if (x >= 0 && x < imageSize && y >= 0 && y < imageSize) {
        pixels[y][x] = true;
        reDraw();
    }
}

void DrawingCanvas::onMouseMove(const gui::Point& point) {
    int x = static_cast<int>((point.x / canvasWidth) * imageSize);
    int y = static_cast<int>((point.y / canvasHeight) * imageSize);
    if (x >= 0 && x < imageSize && y >= 0 && y < imageSize) {
        pixels[y][x] = true;
        reDraw();
    }
}

void DrawingCanvas::clear() {
    for (auto& row : pixels) {
        std::fill(row.begin(), row.end(), false);
    }
    reDraw();
}

Image DrawingCanvas::getImageFromCanvas() {
    Image img(imageSize, imageSize);
    for (int y = 0; y < imageSize; ++y) {
        for (int x = 0; x < imageSize; ++x) {
            img.setPixel(x, y, pixels[y][x] ? 255 : 0);
        }
    }
    return img;
}

void DrawingCanvas::updatePredictions() {
    if (!modelsTrained) {
        return;
    }
    
    Image img = getImageFromCanvas();
    FeatureVector features = featureExtractor.extract(img);
    
    int knnPred = knn.predict(features);
    int nbPred = nb.predict(features);
    int mlpPred = mlp.predict(features);
    int astarPred = astar.match(features);
    int rulePred = rules.predict(img);
    
    reDraw();
}

void DrawingCanvas::drawPredictions() {
}

