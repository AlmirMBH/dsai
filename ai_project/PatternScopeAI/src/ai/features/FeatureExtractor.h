#pragma once
#include "../../data/Image.h"
#include "../../data/FeatureVector.h"

class FeatureExtractor {
public:
    virtual ~FeatureExtractor() {}
    virtual FeatureVector extract(const Image& image) = 0;
};

