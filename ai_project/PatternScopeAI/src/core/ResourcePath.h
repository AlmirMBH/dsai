#pragma once
#include <string>

namespace ResourcePath {

void init(const char* argv0);
std::string getRoot();
std::string getModelsDir();
std::string getMnistDir();
std::string getDatasetsDir();
std::string getTestingSamplesDir();
}
