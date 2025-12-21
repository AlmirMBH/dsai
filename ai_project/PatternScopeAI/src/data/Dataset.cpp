#include "Dataset.h"

/**
 * Add one pattern and its correct category to the collection.
 */
void Dataset::add(const FeatureVector& features, int label) {
    data.push_back(std::make_pair(features, label));
}

/**
 * Retrieve the features of a pattern at a specific position.
 */
const FeatureVector& Dataset::getFeatures(size_t index) const {
    return data[index].first;
}

/**
 * Retrieve the correct category of a pattern at a specific position.
 */
int Dataset::getLabel(size_t index) const {
    return data[index].second;
}

/**
 * Return a list of all categories in the collection.
 */
std::vector<int> Dataset::getLabels() const {
    std::vector<int> labels;
    labels.reserve(data.size());
    for (const auto& pair : data) {
        labels.push_back(pair.second);
    }
    return labels;
}

/**
 * Remove all patterns and categories from the collection.
 */
void Dataset::clear() {
    data.clear();
}

