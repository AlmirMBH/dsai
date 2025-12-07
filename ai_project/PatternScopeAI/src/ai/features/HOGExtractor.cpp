#include "HOGExtractor.h"
#include <cmath>
#include <algorithm>

HOGExtractor::HOGExtractor(int cellSize, int blockSize, int numBins) 
    : cellSize(cellSize), blockSize(blockSize), numBins(numBins) {}

double HOGExtractor::computeGradient(const Image& image, int x, int y, double& magnitude, double& angle) {
    int gx = -static_cast<int>(image.getPixel(x - 1, y)) + static_cast<int>(image.getPixel(x + 1, y));
    int gy = -static_cast<int>(image.getPixel(x, y - 1)) + static_cast<int>(image.getPixel(x, y + 1));
    
    magnitude = std::sqrt(static_cast<double>(gx * gx + gy * gy));
    angle = std::atan2(static_cast<double>(gy), static_cast<double>(gx));
    if (angle < 0) angle += M_PI;
    
    return magnitude;
}

FeatureVector HOGExtractor::extract(const Image& image) {
    int width = image.getWidth();
    int height = image.getHeight();
    
    int cellsX = width / cellSize;
    int cellsY = height / cellSize;
    
    std::vector<std::vector<double>> cellHistograms(cellsY, std::vector<double>(cellsX * numBins, 0.0));
    
    for (int cy = 0; cy < cellsY; ++cy) {
        for (int cx = 0; cx < cellsX; ++cx) {
            int cellStartX = cx * cellSize;
            int cellStartY = cy * cellSize;
            
            for (int y = cellStartY; y < cellStartY + cellSize && y < height - 1; ++y) {
                for (int x = cellStartX; x < cellStartX + cellSize && x < width - 1; ++x) {
                    double magnitude, angle;
                    computeGradient(image, x, y, magnitude, angle);
                    
                    int bin = static_cast<int>((angle / M_PI) * numBins);
                    if (bin >= numBins) bin = numBins - 1;
                    
                    cellHistograms[cy][cx * numBins + bin] += magnitude;
                }
            }
        }
    }
    
    std::vector<double> features;
    
    for (int by = 0; by < cellsY - blockSize + 1; ++by) {
        for (int bx = 0; bx < cellsX - blockSize + 1; ++bx) {
            double blockNorm = 0.0;
            std::vector<double> blockFeatures(blockSize * blockSize * numBins, 0.0);
            
            int idx = 0;
            for (int cy = 0; cy < blockSize; ++cy) {
                for (int cx = 0; cx < blockSize; ++cx) {
                    for (int bin = 0; bin < numBins; ++bin) {
                        double val = cellHistograms[by + cy][(bx + cx) * numBins + bin];
                        blockFeatures[idx++] = val;
                        blockNorm += val * val;
                    }
                }
            }
            
            blockNorm = std::sqrt(blockNorm);
            if (blockNorm > 0) {
                for (double& val : blockFeatures) {
                    val /= blockNorm;
                }
            }
            
            features.insert(features.end(), blockFeatures.begin(), blockFeatures.end());
        }
    }
    
    return FeatureVector(features);
}

