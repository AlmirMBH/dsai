#pragma once
#include <vector>
#include <iostream>

class ConfusionMatrix {
private:
    std::vector<std::vector<int>> matrix;
    int numClasses;
    int totalSamples;

public:
    ConfusionMatrix(int numClasses = 10);
    void addPrediction(int trueLabel, int predictedLabel);
    void reset();
    void print(std::ostream& os) const;
    double getAccuracy() const;
    double getPrecision(int classIndex) const;
    double getRecall(int classIndex) const;
    double getF1Score(int classIndex) const;
    int getTotalSamples() const { return totalSamples; }

    void save(std::ostream& os) const;
    void load(std::istream& is);
};

