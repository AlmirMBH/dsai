#include "AStarMatcher.h"
#include <algorithm>
#include <limits>

double AStarMatcher::heuristic(const FeatureVector& current, const FeatureVector& target) {
    return current.distance(target);
}

void AStarMatcher::addTemplate(const FeatureVector& features, int label) {
    templates.push_back(Template(features, label));
}

void AStarMatcher::buildTemplatesFromDataset(const std::vector<FeatureVector>& features, 
                                             const std::vector<int>& labels) {
    templates.clear();
    if (features.size() != labels.size()) {
        return;
    }
    
    for (size_t i = 0; i < features.size(); ++i) {
        templates.push_back(Template(features[i], labels[i]));
    }
}

int AStarMatcher::match(const FeatureVector& query) {
    if (templates.empty()) {
        return -1;
    }
    
    std::priority_queue<AStarNode, std::vector<AStarNode>, std::greater<AStarNode>> openSet;
    
    for (size_t i = 0; i < templates.size(); ++i) {
        AStarNode node;
        node.templateIndex = i;
        node.gCost = 0.0;
        node.hCost = heuristic(query, templates[i].getFeatures());
        openSet.push(node);
    }
    
    if (openSet.empty()) {
        return -1;
    }
    
    AStarNode best = openSet.top();
    return templates[best.templateIndex].getLabel();
}

double AStarMatcher::getConfidence(const FeatureVector& query) {
    if (templates.empty()) {
        return 0.0;
    }
    
    double minDistance = std::numeric_limits<double>::max();
    double sumDistances = 0.0;
    
    for (const auto& template_ : templates) {
        double dist = template_.distance(query);
        if (dist < minDistance) {
            minDistance = dist;
        }
        sumDistances += dist;
    }
    
    if (sumDistances > 0) {
        return 1.0 / (1.0 + minDistance);
    }
    return 0.0;
}

