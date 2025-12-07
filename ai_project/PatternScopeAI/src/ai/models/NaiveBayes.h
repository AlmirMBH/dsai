#pragma once
#include "Model.h"
#include "../../data/FeatureVector.h"
#include <vector>
#include <cmath>
#include <utility>

class NaiveBayes : public Model {
private:
    std::vector<std::vector<double>> means;
    std::vector<std::vector<double>> variances;
    std::vector<double> priors;
    int numClasses;
    int numFeatures;
    std::vector<std::pair<FeatureVector, int>> incrementalData;

public:
    NaiveBayes();
    void train(const Dataset& dataset) override;
    int predict(const FeatureVector& features) override;
    double getConfidence(const FeatureVector& features) override;
    void updateWithExample(const FeatureVector& features, int label);
    
private:
    double gaussianPDF(double x, double mean, double variance);
};

