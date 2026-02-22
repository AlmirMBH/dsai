#include "ResourcePath.h"
#include <cstdlib>
#include <cstring>
#include <string>

#ifdef _WIN32
#include <windows.h>
#elif defined(__APPLE__)
#include <mach-o/dyld.h>
#include <limits.h>
#include <stdlib.h>
#else
#include <unistd.h>
#endif

namespace ResourcePath {

static std::string s_resourceRoot;

static std::string dirname(const std::string& path) {
    std::string::size_type lastSeparatorPosition = path.find_last_of("/\\");
    if (lastSeparatorPosition == std::string::npos) return ".";
    if (lastSeparatorPosition == 0) return path.substr(0, 1);
    return path.substr(0, lastSeparatorPosition);
}

static std::string getExecutablePath(const char* executablePathArgument) {
    (void)executablePathArgument;
#ifdef _WIN32
    char buffer[MAX_PATH];
    DWORD characterCount = GetModuleFileNameA(NULL, buffer, MAX_PATH);
    if (characterCount == 0 || characterCount >= MAX_PATH) return "";
    return std::string(buffer);
#elif defined(__APPLE__)
    char buffer[PATH_MAX];
    uint32_t bufferSize = sizeof(buffer);
    if (_NSGetExecutablePath(buffer, &bufferSize) != 0) return "";
    char resolvedPath[PATH_MAX];
    if (realpath(buffer, resolvedPath) == nullptr) return buffer;
    return std::string(resolvedPath);
#else
    char buffer[PATH_MAX];
    ssize_t bytesRead = readlink("/proc/self/exe", buffer, sizeof(buffer) - 1);
    if (bytesRead <= 0) return executablePathArgument ? std::string(executablePathArgument) : "";
    buffer[bytesRead] = '\0';
    return std::string(buffer);
#endif
}

void init(const char* executablePathArgument) {
    const char* environmentResourceRoot = std::getenv("PATTERNSCOPE_RESOURCE_ROOT");
    if (environmentResourceRoot && environmentResourceRoot[0] != '\0') {
        s_resourceRoot = environmentResourceRoot;
        if (s_resourceRoot.back() != '/' && s_resourceRoot.back() != '\\')
            s_resourceRoot += "/";
        return;
    }
    std::string executablePath = getExecutablePath(executablePathArgument);
    std::string executableDirectory = dirname(executablePath);

#ifdef __APPLE__
    const std::string macosSuffix = "/Contents/MacOS";
    if (executableDirectory.size() >= macosSuffix.size()) {
        std::string directorySuffix = executableDirectory.substr(executableDirectory.size() - macosSuffix.size());
        if (directorySuffix == macosSuffix) {
            std::string buildDir = dirname(dirname(dirname(executableDirectory)));
            s_resourceRoot = buildDir + "/../resources/";
            return;
        }
    }
#endif
    s_resourceRoot = executableDirectory + "/../resources/";
    if (s_resourceRoot.empty() || (s_resourceRoot.back() != '/' && s_resourceRoot.back() != '\\'))
        s_resourceRoot += "/";
}

std::string getRoot() {
    return s_resourceRoot;
}

std::string getModelsDir() {
    return s_resourceRoot + "models/";
}

std::string getMnistDir() {
    return s_resourceRoot + "mnist/";
}

std::string getDatasetsDir() {
    return s_resourceRoot + "datasets/";
}

std::string getTestingSamplesDir() {
    return s_resourceRoot + "testing_samples/";
}
}
