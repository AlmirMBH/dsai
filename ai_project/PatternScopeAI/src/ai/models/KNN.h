#pragma once
#include "../../data/FeatureVector.h"
#include "../../data/Dataset.h"
#include <vector>
#include <iostream>

class KNN {
    std::vector<std::pair<FeatureVector, int>> trainingData;
    int numberOfNeighbors;

public:
    KNN(int numberOfNeighbors = 3) : numberOfNeighbors(numberOfNeighbors) {}

    void train(const Dataset& dataset);
    void addExample(const FeatureVector& features, int label);
    int predict(const FeatureVector& features);
    double getConfidence(const FeatureVector& features);
    void save(std::ostream& outputStream) const;
    void load(std::istream& inputStream);
};
