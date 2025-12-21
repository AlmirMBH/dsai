#pragma once
#include "../../data/FeatureVector.h"
#include "../../data/Dataset.h"
#include <vector>
#include <iostream>

class KNN {
    std::vector<std::pair<FeatureVector, int>> trainingData;
    int k;

public:
    KNN(int k = 3) : k(k) {}

    void train(const Dataset& dataset);
    void addExample(const FeatureVector& features, int label);
    int predict(const FeatureVector& features);
    double getConfidence(const FeatureVector& features);
    void save(std::ostream& os) const;
    void load(std::istream& is);
};
