#include "Image.h"
#include <algorithm>

Image::Image(int initialWidth, int initialHeight) : width(initialWidth), height(initialHeight) {
    pixels.resize(height, std::vector<uint8_t>(width, 0));
}

Image::Image(int initialWidth, int initialHeight, const std::vector<uint8_t>& data) : width(initialWidth), height(initialHeight) {
    pixels.resize(height, std::vector<uint8_t>(width));
    for (int rowIndex = 0; rowIndex < height; ++rowIndex) {
        for (int columnIndex = 0; columnIndex < width; ++columnIndex) {
            pixels[rowIndex][columnIndex] = data[rowIndex * width + columnIndex];
        }
    }
}

uint8_t Image::getPixel(int columnIndex, int rowIndex) const {
    if (columnIndex >= 0 && columnIndex < width && rowIndex >= 0 && rowIndex < height) {
        return pixels[rowIndex][columnIndex];
    }
    return 0;
}

void Image::setPixel(int columnIndex, int rowIndex, uint8_t value) {
    if (columnIndex >= 0 && columnIndex < width && rowIndex >= 0 && rowIndex < height) {
        pixels[rowIndex][columnIndex] = value;
    }
}

std::vector<uint8_t> Image::getData() const {
    std::vector<uint8_t> data;
    data.reserve(width * height);
    for (const auto& pixelRow : pixels) {
        data.insert(data.end(), pixelRow.begin(), pixelRow.end());
    }
    return data;
}

void Image::normalize() {
    uint8_t maximumPixelValue = 0;
    for (const auto& pixelRow : pixels) {
        for (uint8_t pixelValue : pixelRow) {
            if (pixelValue > maximumPixelValue) {
                maximumPixelValue = pixelValue;
            }
        }
    }
    if (maximumPixelValue > 0) {
        for (auto& pixelRow : pixels) {
            for (uint8_t& pixelValue : pixelRow) {
                pixelValue = (pixelValue * 255) / maximumPixelValue;
            }
        }
    }
}

