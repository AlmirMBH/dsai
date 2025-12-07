#pragma once
#include "Model.h"
#include <vector>
#include <cmath>

class NaiveBayes : public Model {
private:
    std::vector<std::vector<double>> means;
    std::vector<std::vector<double>> variances;
    std::vector<double> priors;
    int numClasses;
    int numFeatures;

public:
    NaiveBayes();
    void train(const Dataset& dataset) override;
    int predict(const FeatureVector& features) override;
    double getConfidence(const FeatureVector& features) override;
    
private:
    double gaussianPDF(double x, double mean, double variance);
};

