#pragma once
#include <vector>
#include <cstdint>

class Image {
private:
    std::vector<std::vector<uint8_t>> pixels;
    int width;
    int height;

public:
    Image(int w, int h);
    Image(int w, int h, const std::vector<uint8_t>& data);
    
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    uint8_t getPixel(int x, int y) const;
    void setPixel(int x, int y, uint8_t value);
    std::vector<uint8_t> getData() const;
    void normalize();
};

