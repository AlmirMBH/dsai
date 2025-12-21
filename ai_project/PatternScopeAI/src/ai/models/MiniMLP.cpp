#include "MiniMLP.h"
#include <random>
#include <algorithm>

/**
 * Adjust the internal weights based on the dataset. 
 * Repeat the process five times to improve accuracy.
 */
void MiniMLP::train(const Dataset& dataset) {
    if (dataset.size() == 0) {
        return;
    }
    std::mt19937 randomGenerator(1337); 
    std::uniform_real_distribution<double> distribution(-0.5, 0.5);
    
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            weights1[hiddenIndex][inputIndex] = distribution(randomGenerator);
        }
        bias1[hiddenIndex] = distribution(randomGenerator);
    }
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            weights2[outputIndex][hiddenIndex] = distribution(randomGenerator);
        }
        bias2[outputIndex] = distribution(randomGenerator);
    }

    double learningRate = 0.01;
    for (int epoch = 0; epoch < 5; epoch++) {
        for (size_t sampleIndex = 0; sampleIndex < dataset.size(); sampleIndex++) {
            std::vector<double> hiddenValues(hiddenSize);
            std::vector<double> outputValues(outputSize);
            
            for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
                double weightedSum = bias1[hiddenIndex];
                for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
                    weightedSum += weights1[hiddenIndex][inputIndex] * dataset.getFeatures(sampleIndex).get(inputIndex);
                }
                hiddenValues[hiddenIndex] = sig(weightedSum);
            }
            for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
                double weightedSum = bias2[outputIndex];
                for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
                    weightedSum += weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex];
                }
                outputValues[outputIndex] = sig(weightedSum);
            }
            
            std::vector<double> targetValues(outputSize, 0.0);
            targetValues[dataset.getLabel(sampleIndex)] = 1.0;
            
            for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
                double outputError = (targetValues[outputIndex] - outputValues[outputIndex]) * outputValues[outputIndex] * (1.0 - outputValues[outputIndex]);
                for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
                    weights2[outputIndex][hiddenIndex] += learningRate * outputError * hiddenValues[hiddenIndex];
                }
                bias2[outputIndex] += learningRate * outputError;
                
                for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
                    double hiddenError = outputError * weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex] * (1.0 - hiddenValues[hiddenIndex]);
                    for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
                        weights1[hiddenIndex][inputIndex] += learningRate * hiddenError * dataset.getFeatures(sampleIndex).get(inputIndex);
                    }
                    bias1[hiddenIndex] += learningRate * hiddenError;
                }
            }
        }
    }
}

/**
 * Update weights using a single new pattern during runtime.
 */
void MiniMLP::addExample(const FeatureVector& features, int label) {
    if (label < 0 || label >= outputSize) {
        return;
    }
    
    double learningRate = 0.01;
    std::vector<double> hiddenValues(hiddenSize);
    std::vector<double> outputValues(outputSize);
    
    // Forward pass
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        double weightedSum = bias1[hiddenIndex];
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            weightedSum += weights1[hiddenIndex][inputIndex] * features.get(inputIndex);
        }
        hiddenValues[hiddenIndex] = sig(weightedSum);
    }
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        double weightedSum = bias2[outputIndex];
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            weightedSum += weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex];
        }
        outputValues[outputIndex] = sig(weightedSum);
    }
    
    // Backward pass (one step)
    std::vector<double> targetValues(outputSize, 0.0);
    targetValues[label] = 1.0;
    
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        double outputError = (targetValues[outputIndex] - outputValues[outputIndex]) * outputValues[outputIndex] * (1.0 - outputValues[outputIndex]);
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            weights2[outputIndex][hiddenIndex] += learningRate * outputError * hiddenValues[hiddenIndex];
        }
        bias2[outputIndex] += learningRate * outputError;
        
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            double hiddenError = outputError * weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex] * (1.0 - hiddenValues[hiddenIndex]);
            for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
                weights1[hiddenIndex][inputIndex] += learningRate * hiddenError * features.get(inputIndex);
            }
            bias1[hiddenIndex] += learningRate * hiddenError;
        }
    }
}

/**
 * Pass the image features through the weighted layers. 
 * Return the category with the strongest signal.
 */
int MiniMLP::predict(const FeatureVector& features) {
    // The hidden layer acts as an intermediate step to find clues in the raw pixels. 
    // These clues help the model recognize complex patterns before deciding on a final category.
    std::vector<double> hiddenValues(hiddenSize);
    std::vector<double> outputValues(outputSize);
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        // A signal is a number that represents how much the model "sees" a certain clue. 
        // We calculate the signal strength for each hidden clue here.
        double weightedSum = bias1[hiddenIndex];
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            weightedSum += weights1[hiddenIndex][inputIndex] * features.get(inputIndex);
        }
        hiddenValues[hiddenIndex] = sig(weightedSum);
    }
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        // Calculate the final signals for each possible category.
        double weightedSum = bias2[outputIndex];
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            weightedSum += weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex];
        }
        outputValues[outputIndex] = sig(weightedSum);
    }
    // Each category (like "Circle" or "7") has its own signal strength. 
    // We find the category with the highest number, which means the strongest match.
    int bestClass = 0;
    for (int classIndex = 1; classIndex < outputSize; classIndex++) {
        if (outputValues[classIndex] > outputValues[bestClass]) {
            bestClass = classIndex;
        }
    }
    return bestClass;
}

/**
 * Calculate certainty by comparing the strongest signal 
 * to the sum of all signals.
 */
double MiniMLP::getConfidence(const FeatureVector& features) {
    std::vector<double> hiddenValues(hiddenSize);
    std::vector<double> outputValues(outputSize);
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        double weightedSum = bias1[hiddenIndex];
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            weightedSum += weights1[hiddenIndex][inputIndex] * features.get(inputIndex);
        }
        hiddenValues[hiddenIndex] = sig(weightedSum);
    }
    double totalOutputSum = 0.0;
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        double weightedSum = bias2[outputIndex];
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            weightedSum += weights2[outputIndex][hiddenIndex] * hiddenValues[hiddenIndex];
        }
        outputValues[outputIndex] = sig(weightedSum);
        totalOutputSum += outputValues[outputIndex];
    }
    // The confidence is calculated by comparing the strongest signal to the total 
    // strength of all signals combined.
    return totalOutputSum > 0 ? outputValues[predict(features)] / totalOutputSum : 0.0;
}

/**
 * Save all internal weights and biases to a text file.
 */
void MiniMLP::save(std::ostream& outputStream) const {
    outputStream << inputSize << " " << hiddenSize << " " << outputSize << "\n";
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            outputStream << weights1[hiddenIndex][inputIndex] << " ";
        }
        outputStream << bias1[hiddenIndex] << "\n";
    }
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            outputStream << weights2[outputIndex][hiddenIndex] << " ";
        }
        outputStream << bias2[outputIndex] << "\n";
    }
}

/**
 * Load weights and biases from a text file.
 */
void MiniMLP::load(std::istream& inputStream) {
    inputStream >> inputSize >> hiddenSize >> outputSize;
    
    // Weights represent the "strength" of connections between sensors and neurons.
    // Bias is an extra adjustment value that helps the network learn patterns more flexibly.
    // Hidden layer is an intermediate step that helps the model find complex relationships in the data.
    weights1.assign(hiddenSize, std::vector<double>(inputSize));
    weights2.assign(outputSize, std::vector<double>(hiddenSize));
    bias1.resize(hiddenSize); 
    bias2.resize(outputSize);
    for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
        for (int inputIndex = 0; inputIndex < inputSize; inputIndex++) {
            inputStream >> weights1[hiddenIndex][inputIndex];
        }
        inputStream >> bias1[hiddenIndex];
    }
    for (int outputIndex = 0; outputIndex < outputSize; outputIndex++) {
        for (int hiddenIndex = 0; hiddenIndex < hiddenSize; hiddenIndex++) {
            inputStream >> weights2[outputIndex][hiddenIndex];
        }
        inputStream >> bias2[outputIndex];
    }
}
