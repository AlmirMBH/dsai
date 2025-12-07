#pragma once
#include "../../data/FeatureVector.h"

class Template {
private:
    FeatureVector features;
    int label;

public:
    Template(const FeatureVector& fv, int lbl);
    const FeatureVector& getFeatures() const { return features; }
    int getLabel() const { return label; }
    double distance(const FeatureVector& other) const;
};

