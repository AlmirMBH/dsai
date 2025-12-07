#pragma once
#include "FeatureExtractor.h"

class PixelGridExtractor : public FeatureExtractor {
private:
    int targetWidth;
    int targetHeight;

public:
    PixelGridExtractor(int width = 28, int height = 28);
    FeatureVector extract(const Image& image) override;
};

