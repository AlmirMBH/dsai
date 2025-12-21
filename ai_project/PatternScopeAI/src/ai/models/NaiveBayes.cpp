#include "NaiveBayes.h"
#include <cmath>
#include <algorithm>

/**
 * Calculate average values and spreads for every pixel 
 * in each category. Store these statistics in memory.
 */
void NaiveBayes::train(const Dataset& dataset) {
    if (dataset.size() == 0) {
        return;
    }
    numFeatures = 784;
    std::vector<int> classCounts(numClasses, 0);
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        means[classIndex].assign(numFeatures, 0.0);
        variances[classIndex].assign(numFeatures, 0.0);
        priors[classIndex] = 0.0;
    }
    
    for (size_t sampleIndex = 0; sampleIndex < dataset.size(); sampleIndex++) {
        int label = dataset.getLabel(sampleIndex);
        classCounts[label]++;
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            means[label][featureIndex] += dataset.getFeatures(sampleIndex).get(featureIndex);
        }
    }
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        priors[classIndex] = (double)classCounts[classIndex] / dataset.size();
        if (classCounts[classIndex] > 0) {
            for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
                means[classIndex][featureIndex] /= classCounts[classIndex];
            }
        }
    }
    
    for (size_t sampleIndex = 0; sampleIndex < dataset.size(); sampleIndex++) {
        int label = dataset.getLabel(sampleIndex);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            double difference = dataset.getFeatures(sampleIndex).get(featureIndex) - means[label][featureIndex];
            variances[label][featureIndex] += difference * difference;
        }
    }
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        if (classCounts[classIndex] > 0) {
            for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
                variances[classIndex][featureIndex] = std::max(1e-9, variances[classIndex][featureIndex] / classCounts[classIndex]);
            }
        }
    }
}

/**
 * Update the stored averages and spreads using one 
 * new pattern during runtime.
 */
void NaiveBayes::addExample(const FeatureVector& features, int label) {
    if (label < 0 || label >= numClasses) {
        return;
    }
    
    totalSamples++;
    double alpha = 1.0 / totalSamples; 
    
    for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
        // Use a mathematical formula (Incremental Update) to adjust the average and spread 
        // without recalculating the entire dataset. Alpha represents the influence of the 
        // new pattern on the existing knowledge.
        double difference = features.get(featureIndex) - means[label][featureIndex];
        means[label][featureIndex] += alpha * difference;
        variances[label][featureIndex] = (1.0 - alpha) * variances[label][featureIndex] + alpha * difference * difference;
        
        // Use 1e-9 (a tiny number) as a floor value to ensure the spread never becomes 
        // exactly zero, which would break future calculations.
        variances[label][featureIndex] = std::max(1e-9, variances[label][featureIndex]);
    }
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        if (classIndex == label) {
            priors[classIndex] = (1.0 - alpha) * priors[classIndex] + alpha;
        } else {
            priors[classIndex] = (1.0 - alpha) * priors[classIndex];
        }
    }
}

/**
 * Calculate the mathematical probability for each 
 * category based on the stored statistics. Return the 
 * category with the highest probability.
 */
int NaiveBayes::predict(const FeatureVector& features) {
    // Start with -1e100 (a extremely small number) so that any real probability 
    // calculated will be larger than this starting point.
    double bestProbability = -1e100;
    int bestClass = 0;
    
    // Use many decimal places for PI to ensure mathematical calculations are accurate.
    const double pi = 3.14159265358979323846;
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        // Start with the log of the initial probability for this category.
        double currentLogProbability = std::log(priors[classIndex] + 1e-10);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            // This is the Bell Curve formula (Gaussian) converted to "Log Space" to prevent numbers 
            // from becoming so small that we lose track of them.
            // 1e-4 is used as a floor to ensure we never divide by zero if the spread is too small.
            double variance = std::max(1e-4, variances[classIndex][featureIndex]);
            double difference = features.get(featureIndex) - means[classIndex][featureIndex];
            currentLogProbability += -0.5 * (std::log(2 * pi * variance) + (difference * difference) / variance);
        }
        if (currentLogProbability > bestProbability) {
            bestProbability = currentLogProbability;
            bestClass = classIndex;
        }
    }
    return bestClass;
}

/**
 * Calculate certainty by comparing the highest 
 * probability to the sum of all probabilities.
 */
double NaiveBayes::getConfidence(const FeatureVector& features) {
    std::vector<double> logProbabilities(numClasses);
    double maxLogProbability = -1e100;
    const double pi = 3.14159265358979323846;
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        logProbabilities[classIndex] = std::log(priors[classIndex] + 1e-10);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            double variance = std::max(1e-4, variances[classIndex][featureIndex]);
            double difference = features.get(featureIndex) - means[classIndex][featureIndex];
            logProbabilities[classIndex] += -0.5 * (std::log(2 * pi * variance) + (difference * difference) / variance);
        }
        if (logProbabilities[classIndex] > maxLogProbability) {
            maxLogProbability = logProbabilities[classIndex];
        }
    }
    
    double sumExponentials = 0.0;
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        sumExponentials += std::exp(std::max(-700.0, logProbabilities[classIndex] - maxLogProbability));
    }
    
    int predictedClass = predict(features);
    double confidence = std::exp(std::max(-700.0, logProbabilities[predictedClass] - maxLogProbability)) / sumExponentials;
    return std::isnan(confidence) ? 0.0 : confidence;
}

/**
 * Save all stored averages, spreads, and counts to a text file.
 */
void NaiveBayes::save(std::ostream& outputStream) const {
    outputStream << numClasses << " " << numFeatures << "\n";
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            outputStream << means[classIndex][featureIndex] << " ";
        }
        outputStream << "\n";
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            outputStream << variances[classIndex][featureIndex] << " ";
        }
        outputStream << "\n";
    }
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        outputStream << priors[classIndex] << " ";
    }
}

/**
 * Load averages, spreads, and counts from a text file.
 */
void NaiveBayes::load(std::istream& inputStream) {
    inputStream >> numClasses >> numFeatures;
    means.resize(numClasses);
    variances.resize(numClasses);
    priors.resize(numClasses);
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        means[classIndex].resize(numFeatures);
        variances[classIndex].resize(numFeatures);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            inputStream >> means[classIndex][featureIndex];
        }
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            inputStream >> variances[classIndex][featureIndex];
        }
    }
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        inputStream >> priors[classIndex];
    }
}
