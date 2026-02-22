#pragma once
#include <vector>
#include <cstdint>

class Image {
private:
    std::vector<std::vector<uint8_t>> pixels;
    int width;
    int height;

public:
    Image(int initialWidth, int initialHeight);
    Image(int initialWidth, int initialHeight, const std::vector<uint8_t>& data);
    
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    uint8_t getPixel(int columnIndex, int rowIndex) const;
    void setPixel(int columnIndex, int rowIndex, uint8_t value);
    std::vector<uint8_t> getData() const;
    void normalize();
};

