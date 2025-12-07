#pragma once
#include <gui/Canvas.h>
#include <gui/Shape.h>
#include <td/ColorID.h>
#include <td/Point.h>
#include <vector>
#include "../data/Image.h"
#include "../ai/features/PixelGridExtractor.h"
#include "../ai/models/KNN.h"
#include "../ai/models/NaiveBayes.h"
#include "../ai/models/MiniMLP.h"
#include "../ai/search/AStarMatcher.h"
#include "../ai/rules/RuleEngine.h"

class DrawingCanvas : public gui::Canvas {
protected:
    std::vector<std::vector<bool>> pixels;
    int canvasWidth;
    int canvasHeight;
    int imageSize;
    
    KNN knn;
    NaiveBayes nb;
    MiniMLP mlp;
    AStarMatcher astar;
    RuleEngine rules;
    PixelGridExtractor featureExtractor;
    bool modelsTrained;
    
    void onResize(const gui::Size& newSize) override;
    void onDraw(const gui::Rect& rect) override;
    void onMouseDown(const gui::Point& point) override;
    void onMouseMove(const gui::Point& point) override;
    
    Image getImageFromCanvas();
    void drawPredictions();

public:
    DrawingCanvas();
    void clear();
    void updatePredictions();
};

