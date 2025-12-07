#include "RuleEngine.h"
#include <algorithm>

RuleEngine::RuleEngine() {
    addRule(Rule{[](const std::vector<double>& f) { return f[0] < 50 && f[1] < 10; }, 1, 0.6});
    addRule(Rule{[](const std::vector<double>& f) { return f[0] > 200 && f[1] > 30; }, 8, 0.7});
    addRule(Rule{[](const std::vector<double>& f) { return f[2] > 1.2; }, 1, 0.5});
    addRule(Rule{[](const std::vector<double>& f) { return f[3] > 0.5; }, 0, 0.6});
    addRule(Rule{[](const std::vector<double>& f) { return f[0] > 100 && f[0] < 150; }, 4, 0.5});
}

void RuleEngine::addRule(const Rule& rule) {
    rules.push_back(rule);
}

int RuleEngine::predict(const Image& image) {
    std::vector<double> features = StructuralFeatures::extractAll(image);
    
    for (const auto& rule : rules) {
        if (rule.condition(features)) {
            return rule.predictedLabel;
        }
    }
    
    return -1;
}

double RuleEngine::getConfidence(const Image& image) {
    std::vector<double> features = StructuralFeatures::extractAll(image);
    
    for (const auto& rule : rules) {
        if (rule.condition(features)) {
            return rule.confidence;
        }
    }
    
    return 0.0;
}

