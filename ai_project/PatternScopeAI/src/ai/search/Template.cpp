#include "Template.h"

Template::Template(const FeatureVector& fv, int lbl) : features(fv), label(lbl) {}

double Template::distance(const FeatureVector& other) const {
    return features.distance(other);
}

