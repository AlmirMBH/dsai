# PatternScope AI

Hybrid pattern recognition (digits, shapes, symbols) using KNN, Naive Bayes, MiniMLP, A* Matcher and a rule-based fallback.

## Mandatory Project Setup (Does not work without these steps)

Data: Download the datasets from `https://drive.google.com/drive/folders/1hYimit3pEeRCuQSTrUa6oRGxfFsd3jKz?usp=sharing` and put datasets in the resources folder as **`resources/mnist/`**, **`resources/datasets/`** and **`resources/testing_samples/`. Paths are exe-relative.

## Build and run

```bash
cd PatternScopeAI &&
mkdir -p build && cd build
cmake .. && make

# 1. Pre-train models (required, takes a few minutes)
./trainer

# 2. Start the app (run from build/ so models are found)
cd PatternScopeAI/build
./PatternVision.app/Contents/MacOS/PatternVision

# Optional: terminal predictor (prompts for image path)
./predictor digits   # or shapes, symbols

# Optional: batch accuracy on test data
./patternScopeAI_cli           # digits
./patternScopeAI_cli shapes    # or symbols
```

If you open the app from elsewhere (e.g. double-click or `open PatternVision.app`) and not as explained above, set `PATTERNSCOPE_RESOURCE_ROOT` to the project **resources** directory first, or the GUI will not find the models that are exported in the resources.

## GUI (PatternVision++)

Mode selection, load image from file, live prediction, per-model comparison, Yes/No feedback. Run from `build/` as above so resource paths match.

**Confusion matrices:** Click **Metrics** to show saved confusion matrices and accuracy per model (KNN, N. Bayes, MLP, A*). Data comes from the last trainer run (stats files in each mode folder). **Accuracy** is the fraction of test samples predicted correctly. The **confusion matrix** has one row per true class and one column per predicted class; cell (i,j) is how often true class i was predicted as j. The diagonal (i,i) is correct predictions for class i; off-diagonal cells are confusions.

## Backend

- **Engine::predict(mode, image)** — ensemble plus fallback; returns `PredictionResult` (finalLabel, finalConfidence, modelComparison).
- **Engine::updateModel(mode, image, correctLabel)** — incremental learning (Yes feedback).
- **Engine::getMetrics(mode, modelName)** — loads saved confusion matrix (e.g. from trainer’s `*_stats.txt`).

Models and stats under `ResourcePath::getModelsDir()` → `resources/models/{digits|shapes|symbols}/`.

## Project details

- Course: Artificial Intelligence, Faculty of Electrical Engineering, University of Sarajevo (Izudin Dzafic)
- Team: Rijalda Sacirbegovic, Almir Mustafic, Tarik Bajrovic
- Stack: C++14, CMake, stb_image, natID
