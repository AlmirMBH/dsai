#include "DrawingCanvas.h"
#include <algorithm>
#include <cmath>
#include <string>

DrawingCanvas::DrawingCanvas() : imageSize(28), modelsTrained(false),
    knnPred(-1), nbPred(-1), mlpPred(-1), astarPred(-1), rulePred(-1),
    knnConf(0.0), nbConf(0.0), mlpConf(0.0), astarConf(0.0), ruleConf(0.0),
    confidenceThreshold(0.6), activeLearningEnabled(true) {
    enableResizeEvent(true);
    pixels.resize(imageSize, std::vector<bool>(imageSize, false));
    canvasWidth = 0;
    canvasHeight = 0;
    trainModels();
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
    
    knnPred = knn.predict(features);
    nbPred = nb.predict(features);
    mlpPred = mlp.predict(features);
    astarPred = astar.match(features);
    rulePred = rules.predict(img);
    
    knnConf = knn.getConfidence(features);
    nbConf = nb.getConfidence(features);
    mlpConf = mlp.getConfidence(features);
    astarConf = astar.getConfidence(features);
    ruleConf = rules.getConfidence(img);
    
    reDraw();
}

void DrawingCanvas::drawPredictions() {
}

void DrawingCanvas::trainModels() {
    std::string trainImagesPath = "../mnist/train-images.idx3-ubyte";
    std::string trainLabelsPath = "../mnist/train-labels.idx1-ubyte";
    std::string testImagesPath = "../mnist/t10k-images.idx3-ubyte";
    std::string testLabelsPath = "../mnist/t10k-labels.idx1-ubyte";
    
    Dataset trainDataset;
    if (!MNISTLoader::loadDataset(trainImagesPath, trainLabelsPath, trainDataset)) {
        modelsTrained = false;
        return;
    }
    
    Dataset smallTrainDataset;
    for (size_t i = 0; i < std::min(trainDataset.size(), size_t(1000)); ++i) {
        smallTrainDataset.add(trainDataset.getFeatures(i), trainDataset.getLabel(i));
    }
    
    knn = KNN(3);
    knn.train(smallTrainDataset);
    
    nb = NaiveBayes();
    nb.train(smallTrainDataset);
    
    mlp = MiniMLP(784, 64, 10);
    mlp.train(smallTrainDataset);
    
    std::vector<Image> images;
    std::vector<int> labels;
    if (MNISTLoader::loadImages(testImagesPath, images) && 
        MNISTLoader::loadLabels(testLabelsPath, labels)) {
        
        std::vector<FeatureVector> templateFeatures;
        std::vector<int> templateLabels;
        
        for (size_t i = 0; i < std::min(images.size(), size_t(100)); ++i) {
            templateFeatures.push_back(featureExtractor.extract(images[i]));
            templateLabels.push_back(labels[i]);
        }
        
        astar.buildTemplatesFromDataset(templateFeatures, templateLabels);
    }
    
    modelsTrained = true;
}

bool DrawingCanvas::isLowConfidence() const {
    if (!modelsTrained) {
        return false;
    }
    
    double avgConf = (knnConf + nbConf + mlpConf + astarConf + ruleConf) / 5.0;
    return avgConf < confidenceThreshold;
}

void DrawingCanvas::updateModelsWithExample(const FeatureVector& features, int label) {
    if (!modelsTrained || label < 0 || label >= 10) {
        return;
    }
    
    knn.addExample(features, label);
    nb.updateWithExample(features, label);
    astar.addTemplate(features, label);
}

FeatureVector DrawingCanvas::getCurrentFeatures() const {
    Image img = getImageFromCanvas();
    return featureExtractor.extract(img);
}

