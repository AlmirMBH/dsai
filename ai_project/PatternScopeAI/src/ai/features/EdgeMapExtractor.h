#pragma once
#include "FeatureExtractor.h"

class EdgeMapExtractor : public FeatureExtractor {
private:
    int targetWidth;
    int targetHeight;

public:
    EdgeMapExtractor(int width = 28, int height = 28);
    FeatureVector extract(const Image& image) override;
    
private:
    double sobelX(const Image& image, int x, int y);
    double sobelY(const Image& image, int x, int y);
};

