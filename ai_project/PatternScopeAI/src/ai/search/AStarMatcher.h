#pragma once
#include "../../data/FeatureVector.h"
#include <vector>
#include <queue>
#include <iostream>

struct AStarNode {
    int templateIndex;
    double gScore;
    double hScore;
    double fScore() const { return gScore + hScore; }
    bool operator>(const AStarNode& other) const { return fScore() > other.fScore(); }
};

class AStarMatcher {
    struct Template {
        FeatureVector features;
        int label;
    };
    std::vector<Template> templates;

public:
    void buildTemplatesFromDataset(const std::vector<FeatureVector>& featureVectors, const std::vector<int>& labels);
    int match(const FeatureVector& query);
    double getConfidence(const FeatureVector& query);
    void save(std::ostream& os) const;
    void load(std::istream& is);
};
