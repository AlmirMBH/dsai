#pragma once
#include "../../data/Image.h"
#include <vector>

class StructuralFeatures {
public:
    static int countEdges(const Image& image);
    static int countCorners(const Image& image);
    static double getAspectRatio(const Image& image);
    static bool hasSymmetry(const Image& image);
    static std::vector<double> extractAll(const Image& image);
};

