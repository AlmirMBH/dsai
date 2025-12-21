#include <iostream>
#include <string>
#include <iomanip>
#include "ai/Engine.h"
#include "data/DataManager.h"

/**
 * Load the pre-trained models and wait for the user to
 * provide an image path. Display the model guess and
 * confidence in the terminal.
 */
int main(int argc, const char* argv[]) {
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
            std::cout << "Prediction: " << result.finalLabel << " | Confidence: " << std::fixed << std::setprecision(2) << result.finalConfidence << " | Model: " << result.finalModelName << std::endl;
        } else {
            std::cout << "Error: Could not load image." << std::endl;
        }
    }
    return 0;
}

