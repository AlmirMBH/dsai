#pragma once
#include "../../data/Dataset.h"
#include "../../data/FeatureVector.h"

class Model {
public:
    virtual ~Model() {}
    virtual void train(const Dataset& dataset) = 0;
    virtual int predict(const FeatureVector& features) = 0;
    virtual double getConfidence(const FeatureVector& features) = 0;
};

