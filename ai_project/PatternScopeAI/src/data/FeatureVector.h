#pragma once
#include <vector>
#include <iostream>

class FeatureVector {
private:
    std::vector<double> features;

public:
    FeatureVector();
    FeatureVector(const std::vector<double>& initialFeatures);
    FeatureVector(size_t size);
    
    size_t size() const { return features.size(); }
    double get(size_t index) const;
    void set(size_t index, double value);
    void add(double value);
    
    void save(std::ostream& outputStream) const;
    void load(std::istream& inputStream);
    
    const std::vector<double>& getFeatures() const { return features; }
    std::vector<double>& getFeatures() { return features; }
    
    double distance(const FeatureVector& other) const;
};

