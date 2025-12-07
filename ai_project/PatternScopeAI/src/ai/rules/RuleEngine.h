#pragma once
#include "StructuralFeatures.h"
#include "../../data/Image.h"
#include <vector>
#include <functional>

struct Rule {
    std::function<bool(const std::vector<double>&)> condition;
    int predictedLabel;
    double confidence;
};

class RuleEngine {
private:
    std::vector<Rule> rules;

public:
    RuleEngine();
    void addRule(const Rule& rule);
    int predict(const Image& image);
    double getConfidence(const Image& image);
};

