#include "NaiveBayes.h"
#include <cmath>
#include <algorithm>

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

void NaiveBayes::addExample(const FeatureVector& features, int label) {
    if (label < 0 || label >= numClasses) {
        return;
    }
    
    totalSamples++;
    double learningRateAlpha = 1.0 / totalSamples; 
    
    for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
        double difference = features.get(featureIndex) - means[label][featureIndex];
        means[label][featureIndex] += learningRateAlpha * difference;
        variances[label][featureIndex] = (1.0 - learningRateAlpha) * variances[label][featureIndex] + learningRateAlpha * difference * difference;
        variances[label][featureIndex] = std::max(1e-9, variances[label][featureIndex]);
    }
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        if (classIndex == label) {
            priors[classIndex] = (1.0 - learningRateAlpha) * priors[classIndex] + learningRateAlpha;
        } else {
            priors[classIndex] = (1.0 - learningRateAlpha) * priors[classIndex];
        }
    }
}

int NaiveBayes::predict(const FeatureVector& features) {
    double bestProbability = -1e100;
    int bestClass = 0;
    const double piConstant = 3.14159265358979323846;
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        double currentLogProbability = std::log(priors[classIndex] + 1e-10);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            double variance = std::max(1e-4, variances[classIndex][featureIndex]);
            double difference = features.get(featureIndex) - means[classIndex][featureIndex];
            currentLogProbability += -0.5 * (std::log(2 * piConstant * variance) + (difference * difference) / variance);
        }
        if (currentLogProbability > bestProbability) {
            bestProbability = currentLogProbability;
            bestClass = classIndex;
        }
    }
    return bestClass;
}

double NaiveBayes::getConfidence(const FeatureVector& features) {
    std::vector<double> logProbabilities(numClasses);
    double maxLogProbability = -1e100;
    const double piConstant = 3.14159265358979323846;
    
    for (int classIndex = 0; classIndex < numClasses; classIndex++) {
        logProbabilities[classIndex] = std::log(priors[classIndex] + 1e-10);
        for (int featureIndex = 0; featureIndex < numFeatures; featureIndex++) {
            double variance = std::max(1e-4, variances[classIndex][featureIndex]);
            double difference = features.get(featureIndex) - means[classIndex][featureIndex];
            logProbabilities[classIndex] += -0.5 * (std::log(2 * piConstant * variance) + (difference * difference) / variance);
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

static const int MAX_NUM_CLASSES = 256;
static const int MAX_NUM_FEATURES = 10000;

void NaiveBayes::load(std::istream& inputStream) {
    int readNumClasses = 0;
    int readNumFeatures = 0;
    inputStream >> readNumClasses >> readNumFeatures;
    if (!inputStream || readNumClasses <= 0 || readNumClasses > MAX_NUM_CLASSES ||
        readNumFeatures <= 0 || readNumFeatures > MAX_NUM_FEATURES) return;
    numClasses = readNumClasses;
    numFeatures = readNumFeatures;
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
