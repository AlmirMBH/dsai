#pragma once
#include "../../data/FeatureVector.h"
#include "../../data/Dataset.h"
#include <vector>
#include <iostream>

class NaiveBayes {
    std::vector<std::vector<double>> means;
    std::vector<std::vector<double>> variances;
    std::vector<double> priors;
    int numClasses;
    int numFeatures;
    int totalSamples;

public:
    NaiveBayes() : numClasses(10), numFeatures(0) { 
        means.resize(numClasses); 
        variances.resize(numClasses); 
        priors.resize(numClasses); 
    }

    void train(const Dataset& dataset);
    void addExample(const FeatureVector& features, int label);
    int predict(const FeatureVector& features);
    double getConfidence(const FeatureVector& features);
    void save(std::ostream& os) const;
    void load(std::istream& is);
};
