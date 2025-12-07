#pragma once
#include "Image.h"
#include "Dataset.h"
#include <string>

class MNISTLoader {
public:
    static bool loadImages(const std::string& imageFile, std::vector<Image>& images);
    static bool loadLabels(const std::string& labelFile, std::vector<int>& labels);
    static bool loadDataset(const std::string& imageFile, const std::string& labelFile, Dataset& dataset);
};

