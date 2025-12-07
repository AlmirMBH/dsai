#pragma once
#include "Model.h"
#include <vector>
#include <utility>
#include <algorithm>
#include <cmath>

class KNN : public Model {
private:
    std::vector<std::pair<FeatureVector, int>> trainingData;
    int k;

public:
    KNN(int k = 3);
    void train(const Dataset& dataset) override;
    int predict(const FeatureVector& features) override;
    double getConfidence(const FeatureVector& features) override;
};

