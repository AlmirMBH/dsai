# PatternScope AI

Hybrid pattern recognition system using machine learning, heuristic search, and rule-based reasoning. It features a unified API, multi-model ensemble voting, and real-world dataset integration.

## How to Run

```bash
cd PatternScopeAI
mkdir -p build && cd build
cmake .. && make

# 1. Pre-train models (Required)
./trainer

# 2. Run recognition
./patternScopeAI          # Digit mode (MNIST)
./patternScopeAI shapes   # Shape mode
./patternScopeAI symbols  # Symbol mode
```

## System Overview

PatternScope AI integrates three core recognition layers:

1.  **Multi-Model Ensemble**:
    - **KNN**: Distance-based classification.
    - **Naive Bayes**: Probabilistic grayscale pattern analysis.
    - **Mini-MLP**: Neural network for nonlinear boundaries.
    - **Active Learning**: Models support incremental updates via `addExample()`.

2.  **Heuristic Search (A*)**:
    - Performs template matching in feature space.
    - Heuristic calculation based on feature vector distances.

3.  **Rule-Based Fallback**:
    - Analyzes structural properties (edge count, corner detection, symmetry).
    - Automatically takes over when machine learning confidence is low.

## Features

- **Multi-Descriptor Extraction**: Uses Pixel Grid, Edge Maps (SIFT-like), and HOG features.
- **Model Comparison**: Real-time visualization of individual model predictions vs. final ensemble decision.
- **Evaluation Metrics**: Full support for Confusion Matrices, Accuracy, Precision, and Recall.
- **Dataset Support**: MNIST (digits), Real hand-drawn datasets (Circle, Square, Triangle, Star, Zigzag, Lightning), and custom image loading (PNG/JPEG).

## Project Details

- **Course**: Artificial Intelligence
- **Faculty**: Faculty of Electrical Engineering, University of Sarajevo
- **Professor**: Izudin Dzafic
- **Team**: Rijalda Sacirbegovic, Almir Mustafic, Tarik Bajrovic
- **Technology**: C++14, CMake, stb_image
