#pragma once
#include "Dataset.h"
#include "Image.h"
#include <string>
#include <vector>

class DataManager {
public:
    static bool loadMNIST(std::string imagePath, std::string labelPath, Dataset& dataset);
    static bool loadImage(std::string path, Image& image);
    static bool loadNumpy(std::string path, Dataset& dataset, int label, int maxSamples);
    static void loadShapes(Dataset& dataset, int samplesPerClass = 500);
    static void loadSymbols(Dataset& dataset, int samplesPerClass = 500);
};

