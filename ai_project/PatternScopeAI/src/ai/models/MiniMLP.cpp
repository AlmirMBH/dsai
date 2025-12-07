#include "MiniMLP.h"
#include <algorithm>

MiniMLP::MiniMLP(int inputSize, int hiddenSize, int outputSize) 
    : inputSize(inputSize), hiddenSize(hiddenSize), outputSize(outputSize) {
    weights1.resize(hiddenSize, std::vector<double>(inputSize));
    weights2.resize(outputSize, std::vector<double>(hiddenSize));
    bias1.resize(hiddenSize, 0.0);
    bias2.resize(outputSize, 0.0);
    initializeWeights();
}

void MiniMLP::initializeWeights() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(-0.5, 0.5);
    
    for (int i = 0; i < hiddenSize; ++i) {
        for (int j = 0; j < inputSize; ++j) {
            weights1[i][j] = dist(gen);
        }
        bias1[i] = dist(gen);
    }
    
    for (int i = 0; i < outputSize; ++i) {
        for (int j = 0; j < hiddenSize; ++j) {
            weights2[i][j] = dist(gen);
        }
        bias2[i] = dist(gen);
    }
}

double MiniMLP::sigmoid(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

double MiniMLP::sigmoidDerivative(double x) {
    double s = sigmoid(x);
    return s * (1.0 - s);
}

void MiniMLP::train(const Dataset& dataset) {
    if (dataset.size() == 0) {
        return;
    }
    
    double learningRate = 0.01;
    int epochs = 10;
    int batchSize = 32;
    
    for (int epoch = 0; epoch < epochs; ++epoch) {
        for (size_t batchStart = 0; batchStart < dataset.size(); batchStart += batchSize) {
            size_t batchEnd = std::min(batchStart + batchSize, dataset.size());
            
            for (size_t i = batchStart; i < batchEnd; ++i) {
                const FeatureVector& input = dataset.getFeatures(i);
                int targetLabel = dataset.getLabel(i);
                
                std::vector<double> hidden(hiddenSize);
                for (int h = 0; h < hiddenSize; ++h) {
                    double sum = bias1[h];
                    for (int j = 0; j < inputSize && j < input.size(); ++j) {
                        sum += weights1[h][j] * input.get(j);
                    }
                    hidden[h] = sigmoid(sum);
                }
                
                std::vector<double> output(outputSize);
                for (int o = 0; o < outputSize; ++o) {
                    double sum = bias2[o];
                    for (int h = 0; h < hiddenSize; ++h) {
                        sum += weights2[o][h] * hidden[h];
                    }
                    output[o] = sigmoid(sum);
                }
                
                std::vector<double> target(outputSize, 0.0);
                if (targetLabel >= 0 && targetLabel < outputSize) {
                    target[targetLabel] = 1.0;
                }
                
                std::vector<double> outputError(outputSize);
                for (int o = 0; o < outputSize; ++o) {
                    outputError[o] = (target[o] - output[o]) * sigmoidDerivative(output[o]);
                }
                
                std::vector<double> hiddenError(hiddenSize);
                for (int h = 0; h < hiddenSize; ++h) {
                    double sum = 0.0;
                    for (int o = 0; o < outputSize; ++o) {
                        sum += weights2[o][h] * outputError[o];
                    }
                    hiddenError[h] = sum * sigmoidDerivative(hidden[h]);
                }
                
                for (int o = 0; o < outputSize; ++o) {
                    for (int h = 0; h < hiddenSize; ++h) {
                        weights2[o][h] += learningRate * outputError[o] * hidden[h];
                    }
                    bias2[o] += learningRate * outputError[o];
                }
                
                for (int h = 0; h < hiddenSize; ++h) {
                    for (int j = 0; j < inputSize && j < input.size(); ++j) {
                        weights1[h][j] += learningRate * hiddenError[h] * input.get(j);
                    }
                    bias1[h] += learningRate * hiddenError[h];
                }
            }
        }
    }
}

int MiniMLP::predict(const FeatureVector& features) {
    if (features.size() != inputSize) {
        return -1;
    }
    
    std::vector<double> hidden(hiddenSize);
    for (int h = 0; h < hiddenSize; ++h) {
        double sum = bias1[h];
        for (int j = 0; j < inputSize; ++j) {
            sum += weights1[h][j] * features.get(j);
        }
        hidden[h] = sigmoid(sum);
    }
    
    std::vector<double> output(outputSize);
    for (int o = 0; o < outputSize; ++o) {
        double sum = bias2[o];
        for (int h = 0; h < hiddenSize; ++h) {
            sum += weights2[o][h] * hidden[h];
        }
        output[o] = sigmoid(sum);
    }
    
    int bestClass = 0;
    double maxOutput = output[0];
    for (int o = 1; o < outputSize; ++o) {
        if (output[o] > maxOutput) {
            maxOutput = output[o];
            bestClass = o;
        }
    }
    
    return bestClass;
}

double MiniMLP::getConfidence(const FeatureVector& features) {
    if (features.size() != inputSize) {
        return 0.0;
    }
    
    std::vector<double> hidden(hiddenSize);
    for (int h = 0; h < hiddenSize; ++h) {
        double sum = bias1[h];
        for (int j = 0; j < inputSize; ++j) {
            sum += weights1[h][j] * features.get(j);
        }
        hidden[h] = sigmoid(sum);
    }
    
    std::vector<double> output(outputSize);
    double sumExp = 0.0;
    for (int o = 0; o < outputSize; ++o) {
        double sum = bias2[o];
        for (int h = 0; h < hiddenSize; ++h) {
            sum += weights2[o][h] * hidden[h];
        }
        output[o] = sigmoid(sum);
        sumExp += output[o];
    }
    
    int predicted = predict(features);
    if (sumExp > 0) {
        return output[predicted] / sumExp;
    }
    return 0.0;
}

