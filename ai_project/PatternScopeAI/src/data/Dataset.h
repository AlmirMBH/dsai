#pragma once
#include "FeatureVector.h"
#include <vector>
#include <string>
#include <utility>

class Dataset {
private:
    std::vector<std::pair<FeatureVector, int>> data;

public:
    void add(const FeatureVector& features, int label);
    size_t size() const { return data.size(); }
    
    const FeatureVector& getFeatures(size_t index) const;
    int getLabel(size_t index) const;
    
    std::vector<int> getLabels() const;
    void clear();
};

