#pragma once
#include "../../data/FeatureVector.h"
#include "../../data/Dataset.h"
#include <vector>
#include <iostream>
#include <cmath>

class MiniMLP {
    int inputSize;
    int hiddenSize;
    int outputSize;
    std::vector<std::vector<double>> weights1;
    std::vector<std::vector<double>> weights2;
    std::vector<double> bias1;
    std::vector<double> bias2;
    
    double sig(double inputValue) { return 1.0 / (1.0 + std::exp(-inputValue)); }

public:
    MiniMLP(int input = 784, int hidden = 64, int output = 10) 
        : inputSize(input), hiddenSize(hidden), outputSize(output) {
        weights1.resize(hiddenSize, std::vector<double>(inputSize)); 
        weights2.resize(outputSize, std::vector<double>(hiddenSize));
        bias1.assign(hiddenSize, 0.0); 
        bias2.assign(outputSize, 0.0);
    }

    void train(const Dataset& dataset);
    void addExample(const FeatureVector& features, int label);
    int predict(const FeatureVector& features);
    double getConfidence(const FeatureVector& features);
    void save(std::ostream& out) const;
    void load(std::istream& in);
};
