#pragma once
#include "FeatureExtractor.h"

class HOGExtractor : public FeatureExtractor {
private:
    int cellSize;
    int blockSize;
    int numBins;

public:
    HOGExtractor(int cellSize = 8, int blockSize = 2, int numBins = 9);
    FeatureVector extract(const Image& image) override;
    
private:
    double computeGradient(const Image& image, int x, int y, double& magnitude, double& angle);
};

