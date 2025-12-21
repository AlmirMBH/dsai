# PatternScope AI

This project is a hybrid pattern recognition system. It processes images to identify digits,
shapes, or symbols. It uses a Hybrid Ensemble of four methods (KNN, Naive Bayes, MiniMLP, and A*
Matcher). If these models are uncertain, the system automatically triggers a Rule-Based Fallback
using structural features.

## Project Setup

The datasets for this project are not included in the repository. Please download them from [Google Drive](https://drive.google.com/drive/folders/1hYimit3pEeRCuQSTrUa6oRGxfFsd3jKz?usp=sharing) and place them in the `mnist/` and `datasets/` folders before building.

```bash
cd PatternScopeAI
mkdir -p build && cd build
cmake .. && make

# 1. Pre-train models (Required - Takes a few minutes)
./trainer

# 2. Run batch recognition test
./patternScopeAI          # Digit mode (MNIST)
./patternScopeAI shapes   # Shape mode
./patternScopeAI symbols  # Symbol mode

# 3. Run real-time image prediction
./predictor digits        # Predict digit from image
./predictor shapes        # Predict shape from image
./predictor symbols       # Predict symbol from image
```

## Real-Time Prediction Testing via Terminal (testing_samples folder)

The real-time predictor tool (`./predictor`) allows users to upload custom images for recognition. 

- **Supported Formats**: PNG, JPEG, BMP.
- **Testing Samples**: Sample images are provided in the `testing_samples/` folder.
- **Requirements**: Images are automatically resized to 28x28 and normalized (0.0 to 1.0) before processing.
- **Workflow**: Run the predictor and enter the relative path to an image when prompted. Note: The first prediction takes time (several minutes) to load model data into memory; subsequent tests are instant.
  - If running from the `build/` folder, use: `../testing_samples/sample_a.png`
  - If running from the `PatternScopeAI/` folder, use: `testing_samples/sample_a.png`


## Backend-Frontend (natID) Integration Guide

All models functionality is exposed through the `Engine` class (located in `src/ai/Engine.h` and `src/ai/Engine.cpp`).

### A. Making a Prediction
- **Function**: `src/ai/Engine::predict(Mode mode, const Image& image)`
- **Logic**: Runs all models, calculates an ensemble decision, and triggers Rule-Based fallback if confidence is low (< 0.4).
- **Confidence Note**: The final confidence is an average of all 4 models. We prefer "honest" low scores over "fake" high scores; a high score only appears if multiple models strongly agree on the result.
- **Output (`PredictionResult`)**:
    - `finalLabel`: The winning category index (int).
    - `finalConfidence`: Overall agreement score (0.0 to 1.0).
    - `finalModelName`: "Hybrid Ensemble" or "RuleEngine (Fallback)".
    - `modelComparison`: A map containing individual results for every model.

### B. Active Learning (Updating Models)
- **Function**: `src/ai/Engine::updateModel(Mode mode, const Image& image, int correctLabel)`
- **Logic**: Implements the "Active-Learning Agent" by adding the new example to KNN, Naive Bayes, and MiniMLP datasets incrementally.

### C. Retrieving Performance Metrics
- **Function**: `src/ai/Engine::getMetrics(Mode mode, string modelName)`
- **Usage**: Returns accuracy, precision, recall, and F1-score for the specified model and mode.

## Project Lifecycle & Dataflow

The project follows a specific multi-step process from data acquisition to real-time recognition.

### 1. Data Management Utilities
The `DataManager` class (located in `src/data/DataManager.h` and `src/data/DataManager.cpp`) handles all dataset interactions:
- **`loadImage(string path, Image& image)`**: Loads a PNG, JPEG, or BMP from disk.
- **`loadMNIST(...)`**: Loads raw MNIST digit files from the `mnist/` folder.
- **`loadShapes/loadSymbols(...)`**: Loads real hand-drawn patterns from the `datasets/` folder (.npy files).

### 2. Detailed Dataflow Steps

#### STEP 1: Data Acquisition & Processing
During initialization, the system fetches three types of datasets:
- **Digits**: Fetched from the local `mnist/` folder.
- **Shapes & Symbols**: Fetched from the `datasets/` folder.
These are processed by `src/data/DataManager::loadNumpy()` into normalized `FeatureVector` objects.

#### STEP 2: Model Training
The `./trainer` tool (`src/trainer.cpp`) initializes the training phase. Each model creates its internal logic:
- **KNN**: Stores a library of training patterns for distance comparison.
- **Naive Bayes**: Calculates statistical means and variances for probabilistic analysis.
- **MiniMLP**: Learns weight and bias matrices via backpropagation.
- **A* Matcher**: Selects optimal templates for heuristic-based matching.

#### STEP 3: Serialization (Generating Model Files)
Once training is finished, the system generates text-based model files in `build/models/`:
- `knn.txt`: Contains the library of features and labels.
- `nb.txt`: Contains the calculated probabilities, means, and variances.
- `mlp.txt`: Contains the trained weight matrices and bias vectors.
- `astar.txt`: Contains the selected templates used for matching.

#### STEP 4: Evaluation & Performance Storage
After saving models, the system evaluates performance using test data and generates stats files (e.g., `knn_stats.txt`). These store the Confusion Matrix and accuracy data used for model comparison.

#### STEP 5: Runtime Prediction & Active Learning
When a user uploads an image or draws on the canvas:
1.  **Ensemble Prediction**: The image is passed to `src/ai/Engine::predict()`, which runs all models.
2.  **Fallback Logic**: If overall confidence is low, the **Rule-Based Fallback** is triggered.
3.  **Active Learning**: If the user provides the "Correct Label", the system calls `src/ai/Engine::updateModel()`. This adds the new sample to the models' memory instantly (**Incremental Learning**), making it smarter without needing a full re-train.

## Project Details

- **Course**: Artificial Intelligence
- **Faculty**: Faculty of Electrical Engineering, University of Sarajevo
- **Professor**: Izudin Dzafic
- **Team**: Rijalda Sacirbegovic, Almir Mustafic, Tarik Bajrovic
- **Technology**: C++14, CMake, stb_image
