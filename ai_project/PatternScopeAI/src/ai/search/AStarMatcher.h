#pragma once
#include "Template.h"
#include "../../data/FeatureVector.h"
#include <vector>
#include <queue>
#include <cmath>

struct AStarNode {
    int templateIndex;
    double gCost;
    double hCost;
    double fCost() const { return gCost + hCost; }
    
    bool operator>(const AStarNode& other) const {
        return fCost() > other.fCost();
    }
};

class AStarMatcher {
private:
    std::vector<Template> templates;
    
    double heuristic(const FeatureVector& current, const FeatureVector& target);

public:
    void addTemplate(const FeatureVector& features, int label);
    void buildTemplatesFromDataset(const std::vector<FeatureVector>& features, 
                                   const std::vector<int>& labels);
    int match(const FeatureVector& query);
    double getConfidence(const FeatureVector& query);
};

