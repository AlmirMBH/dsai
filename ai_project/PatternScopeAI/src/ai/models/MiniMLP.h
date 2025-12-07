#pragma once
#include "Model.h"
#include <vector>
#include <cmath>
#include <random>

class MiniMLP : public Model {
private:
    int inputSize;
    int hiddenSize;
    int outputSize;
    
    std::vector<std::vector<double>> weights1;
    std::vector<std::vector<double>> weights2;
    std::vector<double> bias1;
    std::vector<double> bias2;
    
    double sigmoid(double x);
    double sigmoidDerivative(double x);
    void initializeWeights();

public:
    MiniMLP(int inputSize = 784, int hiddenSize = 64, int outputSize = 10);
    void train(const Dataset& dataset) override;
    int predict(const FeatureVector& features) override;
    double getConfidence(const FeatureVector& features) override;
};

