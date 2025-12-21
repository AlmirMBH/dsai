#include "Image.h"
#include <algorithm>

Image::Image(int w, int h) : width(w), height(h) {
    pixels.resize(height, std::vector<uint8_t>(width, 0));
}

Image::Image(int w, int h, const std::vector<uint8_t>& data) : width(w), height(h) {
    pixels.resize(height, std::vector<uint8_t>(width));
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            pixels[y][x] = data[y * width + x];
        }
    }
}

/**
 * Retrieve the brightness of a pixel at specific coordinates.
 */
uint8_t Image::getPixel(int x, int y) const {
    if (x >= 0 && x < width && y >= 0 && y < height) {
        return pixels[y][x];
    }
    return 0;
}

/**
 * Set the brightness of a pixel at specific coordinates.
 */
void Image::setPixel(int x, int y, uint8_t value) {
    if (x >= 0 && x < width && y >= 0 && y < height) {
        pixels[y][x] = value;
    }
}

/**
 * Convert the image grid into a single long list of pixels.
 */
std::vector<uint8_t> Image::getData() const {
    std::vector<uint8_t> data;
    data.reserve(width * height);
    for (const auto& row : pixels) {
        data.insert(data.end(), row.begin(), row.end());
    }
    return data;
}

/**
 * Stretch the light values so the darkest pixel is 0 
 * and the brightest is 255. This makes the image clearer for the models.
 */
void Image::normalize() {
    uint8_t maxVal = 0;
    for (const auto& row : pixels) {
        for (uint8_t val : row) {
            if (val > maxVal) {
                maxVal = val;
            }
        }
    }
    if (maxVal > 0) {
        for (auto& row : pixels) {
            for (uint8_t& val : row) {
                val = (val * 255) / maxVal;
            }
        }
    }
}

