#include "NaiveBayes.h"
#include <algorithm>

NaiveBayes::NaiveBayes() : numClasses(10), numFeatures(0) {
    means.resize(numClasses);
    variances.resize(numClasses);
    priors.resize(numClasses, 0.0);
}

double NaiveBayes::gaussianPDF(double x, double mean, double variance) {
    if (variance < 1e-9) {
        variance = 1e-9;
    }
    double diff = x - mean;
    return std::exp(-(diff * diff) / (2.0 * variance)) / std::sqrt(2.0 * M_PI * variance);
}

void NaiveBayes::train(const Dataset& dataset) {
    if (dataset.size() == 0) {
        return;
    }
    
    numFeatures = dataset.getFeatures(0).size();
    
    for (int c = 0; c < numClasses; ++c) {
        means[c].resize(numFeatures, 0.0);
        variances[c].resize(numFeatures, 0.0);
    }
    
    std::vector<int> classCounts(numClasses, 0);
    
    for (size_t i = 0; i < dataset.size(); ++i) {
        int label = dataset.getLabel(i);
        if (label >= 0 && label < numClasses) {
            classCounts[label]++;
            const FeatureVector& fv = dataset.getFeatures(i);
            for (int j = 0; j < numFeatures; ++j) {
                means[label][j] += fv.get(j);
            }
        }
    }
    
    for (int c = 0; c < numClasses; ++c) {
        if (classCounts[c] > 0) {
            priors[c] = static_cast<double>(classCounts[c]) / dataset.size();
            for (int j = 0; j < numFeatures; ++j) {
                means[c][j] /= classCounts[c];
            }
        }
    }
    
    for (size_t i = 0; i < dataset.size(); ++i) {
        int label = dataset.getLabel(i);
        if (label >= 0 && label < numClasses) {
            const FeatureVector& fv = dataset.getFeatures(i);
            for (int j = 0; j < numFeatures; ++j) {
                double diff = fv.get(j) - means[label][j];
                variances[label][j] += diff * diff;
            }
        }
    }
    
    for (int c = 0; c < numClasses; ++c) {
        if (classCounts[c] > 0) {
            for (int j = 0; j < numFeatures; ++j) {
                variances[c][j] /= classCounts[c];
                if (variances[c][j] < 1e-9) {
                    variances[c][j] = 1e-9;
                }
            }
        }
    }
}

int NaiveBayes::predict(const FeatureVector& features) {
    if (numFeatures == 0 || features.size() != numFeatures) {
        return -1;
    }
    
    std::vector<double> posteriors(numClasses, 0.0);
    
    for (int c = 0; c < numClasses; ++c) {
        double likelihood = std::log(priors[c] + 1e-10);
        for (int j = 0; j < numFeatures; ++j) {
            double prob = gaussianPDF(features.get(j), means[c][j], variances[c][j]);
            likelihood += std::log(prob + 1e-10);
        }
        posteriors[c] = likelihood;
    }
    
    int bestClass = 0;
    double maxPosterior = posteriors[0];
    for (int c = 1; c < numClasses; ++c) {
        if (posteriors[c] > maxPosterior) {
            maxPosterior = posteriors[c];
            bestClass = c;
        }
    }
    
    return bestClass;
}

double NaiveBayes::getConfidence(const FeatureVector& features) {
    if (numFeatures == 0 || features.size() != numFeatures) {
        return 0.0;
    }
    
    std::vector<double> posteriors(numClasses, 0.0);
    
    for (int c = 0; c < numClasses; ++c) {
        double likelihood = std::log(priors[c] + 1e-10);
        for (int j = 0; j < numFeatures; ++j) {
            double prob = gaussianPDF(features.get(j), means[c][j], variances[c][j]);
            likelihood += std::log(prob + 1e-10);
        }
        posteriors[c] = likelihood;
    }
    
    double maxPosterior = posteriors[0];
    double sumExp = 0.0;
    for (int c = 0; c < numClasses; ++c) {
        if (posteriors[c] > maxPosterior) {
            maxPosterior = posteriors[c];
        }
    }
    
    for (int c = 0; c < numClasses; ++c) {
        sumExp += std::exp(posteriors[c] - maxPosterior);
    }
    
    return std::exp(posteriors[predict(features)] - maxPosterior) / sumExp;
}

