#pragma once
#include "../../data/Image.h"
#include <vector>
#include <functional>

struct RecognitionRule {
    std::function<bool(const std::vector<double>&)> condition;
    int label;
    double confidence;
};

class RuleEngine {
    std::vector<RecognitionRule> rules;
    std::vector<double> extractFeatures(const Image& image);

public:
    RuleEngine();
    int predict(const Image& image);
    double getConfidence(const Image& image);
};
