#include <iostream>
#include <string>
#include <iomanip>
#include "core/ResourcePath.h"
#include "ai/Engine.h"
#include "data/DataManager.h"

int main(int argc, const char* argv[]) {
    ResourcePath::init(argc > 0 ? argv[0] : "predictor");
    if (argc < 2) {
        std::cout << "Usage: ./predictor <digits|shapes|symbols>" << std::endl;
        return 1;
    }

    std::string modeArgument = argv[1];
    Mode recognitionMode;
    if (modeArgument == "digits") {
        recognitionMode = Mode::DIGITS;
    } else if (modeArgument == "shapes") {
        recognitionMode = Mode::SHAPES;
    } else if (modeArgument == "symbols") {
        recognitionMode = Mode::SYMBOLS;
    } else {
        std::cout << "Unknown mode." << std::endl;
        return 1;
    }

    Engine recognitionEngine;
    std::string inputPath;
    while (true) {
        std::cout << "Enter image path (or 'exit' to quit): ";
        std::cin >> inputPath;
        if (inputPath == "exit") {
            break;
        }

        Image userImage(28, 28);
        if (DataManager::loadImage(inputPath, userImage)) {
            userImage.normalize();
            auto result = recognitionEngine.predict(recognitionMode, userImage);
            std::string labelStr = (recognitionMode == Mode::DIGITS && result.finalLabel >= 0 && result.finalLabel <= 9)
                ? std::string(1, '0' + result.finalLabel) : std::to_string(result.finalLabel);
            std::cout << "Top class: " << labelStr << ", Confidence: " << std::fixed << std::setprecision(2) << result.finalConfidence << ", Model: " << result.finalModelName << std::endl;
            std::cout << "Model Comparison" << std::endl;
            static const char* modelKeys[] = {"KNN", "NaiveBayes", "MiniMLP", "AStar", "RuleEngine"};
            static const char* modelDisplayNames[] = {"KNN", "N. Bayes", "MLP", "A*", "Fallback"};
            for (int index = 0; index < 5; ++index) {
                auto it = result.modelComparison.find(modelKeys[index]);
                if (it != result.modelComparison.end())
                    std::cout << modelDisplayNames[index] << ": " << it->second.label << ", Confidence: " << std::fixed << std::setprecision(2) << it->second.confidence << std::endl;
            }
        } else {
            std::cout << "Error: Could not load image." << std::endl;
        }
    }
    return 0;
}

