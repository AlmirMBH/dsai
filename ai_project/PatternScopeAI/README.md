# PatternScope AI

Hybrid pattern recognition system combining machine learning models, A* template matching, and rule-based reasoning for digit, shape, and symbol recognition (C++14 required).

## Project Background

This project was completed as part of the undergraduate course _Artificial Intelligence_ at the Faculty of Electrical Engineering, University of Sarajevo, under the supervision of Professor Izudin Dzafic. The system implements machine learning models (KNN, Naive Bayes, Mini-MLP), A* search for template matching, and rule-based reasoning. It recognizes MNIST digits, geometric shapes, and user-drawn symbols, with console and GUI interfaces.

## Project Team

- **Rijalda Sacirbegovic**
- **Almir Mustafic**
- **Tarik Bajrovic**

## Technologies

- **C++14**: Programming language
- **CMake**: Build system
- **natID**: GUI framework (optional, requires separate setup)
- **MNIST Dataset**: Digit recognition dataset (60,000 training, 10,000 test samples)

## How to Run

### Console Version

```bash
cd PatternScopeAI
mkdir -p build
cd build
cmake ..
make
./patternScopeAI
```

### Run Tests

```bash
cd PatternScopeAI/build
./test_all
```

### GUI Version

Requires natID setup in `${HOME}/Work/DevEnv/`:

```bash
cd PatternScopeAI
mkdir -p build
cd build
cmake -f ../CMakeLists_GUI.txt ..
make
```

## Project Structure

```
PatternScopeAI/
├── src/
│   ├── ai/
│   │   ├── models/      # ML models (KNN, NaiveBayes, MiniMLP)
│   │   ├── features/    # Feature extraction (PixelGrid, EdgeMap, HOG)
│   │   ├── search/      # A* template matching
│   │   └── rules/       # Rule-based reasoning
│   ├── data/
│   │   ├── Image.h/cpp
│   │   ├── FeatureVector.h/cpp
│   │   ├── Dataset.h/cpp
│   │   ├── MNISTLoader.h/cpp
│   │   └── ConfusionMatrix.h/cpp
│   ├── gui/             # GUI components (requires natID)
│   │   ├── Application.h
│   │   ├── MainWindow.h
│   │   ├── MainView.h/cpp
│   │   └── DrawingCanvas.h/cpp
│   └── main.cpp
├── build/
├── mnist/               # MNIST dataset files
├── CMakeLists.txt       # Console version
├── CMakeLists_GUI.txt   # GUI version
└── test_all.cpp
```

## Core AI Components

### 1. Multi-Model Classification Engine
Three machine learning models:
- **KNN**: Distance-based classifier
- **Naive Bayes**: Probabilistic classifier
- **Mini-MLP**: Neural network with one hidden layer

### 2. Feature Extraction Module
Three descriptor types:
- **PixelGrid**: Pixel grid (784 features for 28x28 images)
- **EdgeMap**: Edge detection (784 features)
- **HOG**: Histogram of Oriented Gradients (144 features)

### 3. A* Template Matching
- Templates as feature vectors
- Heuristic: feature vector distance
- Deterministic decisions

### 4. Rule-Based Reasoning
- Edge count, corner detection, structural properties
- Fallback when ML confidence is low
- Features: edges, corners, aspect ratio, symmetry

### 5. Active Learning
- Confidence threshold detection
- User feedback collection for low-confidence predictions
- Incremental model updates (KNN, NaiveBayes, A*)

### 6. Evaluation Metrics
- Confusion matrix calculation and display
- Per-class precision, recall, F1-score
- Model comparison and analysis


## Dataset

MNIST dataset files in `mnist/` directory:
- `train-images.idx3-ubyte`
- `train-labels.idx1-ubyte`
- `t10k-images.idx3-ubyte`
- `t10k-labels.idx1-ubyte`

Path: `../mnist/` relative to build directory.

## Known Limitations

- GUI requires natID framework setup
- Dataset path: `../mnist/` relative to build directory
- Models trained on 1000 samples subset
- HOG implementation simplified
- Rule-based reasoning provides basic structural analysis

## Next Steps

- Train on full MNIST dataset
- Implement additional feature extractors (SIFT, SURF)
- Combine predictions with weighted voting
- Complete natID GUI integration
- Extend to geometric shapes and custom symbols
- Add confusion matrix visualization to GUI

## Contact

- **Rijalda Sacirbegovic**
- **Almir Mustafic** — [GitHub](https://github.com/AlmirMBH)
- **Tarik Bajrovic**

## License

MIT License

## Acknowledgments

- **MNIST Dataset**: Modified National Institute of Standards and Technology database
- **CMake**: BSD 3-Clause License
- **natID**: GUI framework (requires separate license)

Special thanks to Professor Izudin Dzafic for guidance during the Artificial Intelligence course.

## Disclaimer

This project is an academic exercise completed as part of the Artificial Intelligence course. It demonstrates machine learning, heuristic search, and rule-based reasoning techniques for educational purposes.
