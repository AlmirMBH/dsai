#include "AStarMatcher.h"
#include <algorithm>

/**
 * Store a subset of patterns from the dataset to use 
 * as fixed templates for matching.
 */
void AStarMatcher::buildTemplatesFromDataset(const std::vector<FeatureVector>& featureVectors, const std::vector<int>& labels) {
    templates.clear();
    for (size_t templateIndex = 0; templateIndex < featureVectors.size(); templateIndex++) {
        templates.push_back({featureVectors[templateIndex], labels[templateIndex]});
    }
}

/**
 * Search for the template that is mathematically 
 * closest to the new image features. Return the category 
 * of the best match.
 */
int AStarMatcher::match(const FeatureVector& query) {
    if (templates.empty()) {
        return -1;
    }
    
    std::priority_queue<AStarNode, std::vector<AStarNode>, std::greater<AStarNode>> openList;
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        double distance = query.distance(templates[templateIndex].features);
        openList.push({templateIndex, 0.0, distance});
    }
    
    return templates[openList.top().templateIndex].label;
}

/**
 * Calculate certainty based on the mathematical 
 * distance to the best template match.
 */
double AStarMatcher::getConfidence(const FeatureVector& query) {
    if (templates.empty()) {
        return 0.0;
    }
    
    // Start with a very large distance (1e10) so any real distance found is smaller.
    double minDistanceValue = 1e10;
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        double currentDistance = templates[templateIndex].features.distance(query);
        if (currentDistance < minDistanceValue) {
            minDistanceValue = currentDistance;
        }
    }
    // Convert the distance to a score between 0 and 1. A small distance means the model 
    // is more certain (closer to 1.0).
    return 1.0 / (1.0 + minDistanceValue);
}

/**
 * Save all stored templates to a text file.
 */
void AStarMatcher::save(std::ostream& outputStream) const {
    outputStream << templates.size() << "\n";
    for (int templateIndex = 0; templateIndex < (int)templates.size(); templateIndex++) {
        for (double featureValue : templates[templateIndex].features.getFeatures()) {
            outputStream << featureValue << " ";
        }
        outputStream << templates[templateIndex].label << "\n";
    }
}

/**
 * Load templates from a text file into memory.
 */
void AStarMatcher::load(std::istream& inputStream) {
    size_t numTemplates;
    inputStream >> numTemplates;
    templates.clear();
    for (size_t templateIndex = 0; templateIndex < numTemplates; templateIndex++) {
        std::vector<double> featureValues(784);
        for (int featureIndex = 0; featureIndex < 784; featureIndex++) {
            inputStream >> featureValues[featureIndex];
        }
        int labelValue;
        inputStream >> labelValue;
        templates.push_back({FeatureVector(featureValues), labelValue});
    }
}
