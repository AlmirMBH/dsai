#include "AStarMatcher.h"
#include <algorithm>

void AStarMatcher::buildTemplatesFromDataset(const std::vector<FeatureVector>& featureVectors, const std::vector<int>& labels) {
    templates.clear();
    for (size_t templateIndex = 0; templateIndex < featureVectors.size(); templateIndex++) {
        templates.push_back({featureVectors[templateIndex], labels[templateIndex]});
    }
}

int AStarMatcher::match(const FeatureVector& query) {
    if (templates.empty()) return -1;
    
    std::priority_queue<AStarNode, std::vector<AStarNode>, std::greater<AStarNode>> openList;
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        double distance = query.distance(templates[templateIndex].features);
        openList.push({templateIndex, 0.0, distance});
    }
    
    return templates[openList.top().templateIndex].label;
}

double AStarMatcher::getConfidence(const FeatureVector& query) {
    if (templates.empty()) return 0.0;
    
    double minDistanceValue = 1e10;
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        double currentDistance = templates[templateIndex].features.distance(query);
        if (currentDistance < minDistanceValue) minDistanceValue = currentDistance;
    }
    return 1.0 / (1.0 + minDistanceValue);
}

void AStarMatcher::save(std::ostream& outputStream) const {
    outputStream << templates.size() << "\n";
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        for (double featureValue : templates[templateIndex].features.getFeatures()) outputStream << featureValue << " ";
        outputStream << templates[templateIndex].label << "\n";
    }
}

void AStarMatcher::load(std::istream& inputStream) {
    size_t numTemplates;
    inputStream >> numTemplates;
    templates.clear();
    for (size_t templateIndex = 0; templateIndex < numTemplates; templateIndex++) {
        std::vector<double> featureValues(784);
        for (int featureIndex = 0; featureIndex < 784; featureIndex++) inputStream >> featureValues[featureIndex];
        int labelValue;
        inputStream >> labelValue;
        templates.push_back({FeatureVector(featureValues), labelValue});
    }
}
