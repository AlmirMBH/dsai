#include "MainView.h"
#include "FileDialog.h"
#include <gui/HorizontalLayout.h>
#include <gui/VerticalLayout.h>
#include <td/ColorID.h>
#include <string>
#include <iomanip>
#include <sstream>

MainView::MainView()
: btnDigits("Digits (0-9)"),
  btnShapes("Geometric Shapes"),
  btnSymbols("Custom Symbols"),
  lblPredictionTitle("Predictions"),
  lblTopRow("Top class: -, Confidence: 0.00"),
  lblComparisonTitle("Model Comparison"),
  lblKNN("KNN: -, Confidence: -"),
  lblNaiveBayes("N. Bayes: -, Confidence: -"),
  lblMLP("MLP: -, Confidence: -"),
  lblAStar("A*: -, Confidence: -"),
  lblRuleFallback("Fallback: -, Confidence: -"),
  btnLoadImage("Load Image"),
  btnClear("Clear"),
  btnMetrics("Metrics"),
  lblFeedback("Is the prediction OK?"),
  btnCorrect("Yes"),
  btnIncorrect("No"),
  modeBarLayout(3),
  predictionFrameView(30, 30, 30, 30),
  feedbackFrameView(10, 20, 10, 20),
  metricsFrameView(10, 20, 10, 20),
  lblMetricsTitle("Confusion matrices (click Metrics to load)"),
  lblMetricsKNN("KNN: -"),
  lblMetricsNaiveBayes("N. Bayes: -"),
  lblMetricsMLP("MLP: -"),
  lblMetricsAStar("A*: -"),
  predictionPanel(9),
  feedbackVerticalLayout(2),
  feedbackButtonsLayout(2),
  rightLayout(3),
  metricsPanelLayout(6),
  footerLayout(3),
  mainLayout(3)
{
    modeBarLayout.append(btnDigits);
    modeBarLayout.append(btnShapes);
    modeBarLayout.append(btnSymbols);
    mainLayout.append(modeBarLayout);

    predictionPanel.append(lblPredictionTitle);
    predictionPanel.append(lblTopRow);
    predictionPanel.append(lblComparisonTitle);
    predictionPanel.append(lblKNN);
    predictionPanel.append(lblNaiveBayes);
    predictionPanel.append(lblMLP);
    predictionPanel.append(lblAStar);
    predictionPanel.append(lblRuleFallback);
    predictionFrameView.setLayout(&predictionPanel);
    predictionFrameView.setBackgroundColor(td::ColorID::LightGray);
    rightLayout.append(predictionFrameView);

    feedbackVerticalLayout.append(lblFeedback);
    feedbackButtonsLayout.append(btnCorrect);
    feedbackButtonsLayout.append(btnIncorrect);
    feedbackVerticalLayout.append(feedbackButtonsLayout);
    feedbackFrameView.setLayout(&feedbackVerticalLayout);
    feedbackFrameView.setBackgroundColor(td::ColorID::LightGray);
    rightLayout.append(feedbackFrameView);

    metricsPanelLayout.append(lblMetricsTitle);
    metricsPanelLayout.append(lblMetricsKNN);
    metricsPanelLayout.append(lblMetricsNaiveBayes);
    metricsPanelLayout.append(lblMetricsMLP);
    metricsPanelLayout.append(lblMetricsAStar);
    metricsFrameView.setLayout(&metricsPanelLayout);
    metricsFrameView.setBackgroundColor(td::ColorID::LightGray);
    rightLayout.append(metricsFrameView);

    mainLayout.append(rightLayout);

    footerLayout.append(btnLoadImage);
    footerLayout.append(btnClear);
    footerLayout.append(btnMetrics);
    mainLayout.append(footerLayout);

    _modelLabels[0] = &lblKNN;
    _modelLabels[1] = &lblNaiveBayes;
    _modelLabels[2] = &lblMLP;
    _modelLabels[3] = &lblAStar;
    _modelLabels[4] = &lblRuleFallback;

    setLayout(&mainLayout);
}

static const char* _modelDisplayNames[] = {"KNN", "N. Bayes", "MLP", "A*", "Fallback"};

void MainView::clearPredictionLabels() {
    lblTopRow.setTitle("Top class: -, Confidence: 0.00");
    for (unsigned index = 0; index < _modelCount; ++index)
        _modelLabels[index]->setTitle(std::string(_modelDisplayNames[index]) + ": -, Confidence: -");
    lblFeedback.setTitle("Is the prediction OK?");
    _hasPrediction = false;
}

bool MainView::onClick(gui::Button* button) {
    if (button == &btnLoadImage) {
        std::string path = openImageFile();
        if (path.empty()) {
            return true;
        }
        if (!DataManager::loadImage(path, _currentImage)) {
            lblTopRow.setTitle("Load failed");
            return true;
        }
        _currentImagePath = path;
        _currentImage.normalize();
        _hasPrediction = false;
        clearPredictionLabels();
        return true;
    }
    if (button == &btnDigits || button == &btnShapes || button == &btnSymbols) {
        if (_currentImagePath.empty()) {
            lblTopRow.setTitle("Load an image first.");
            return true;
        }
        Mode mode = (button == &btnDigits) ? Mode::DIGITS : (button == &btnShapes) ? Mode::SHAPES : Mode::SYMBOLS;
        PredictionResult result = _engine.predict(mode, _currentImage);
        _hasPrediction = true;
        _lastMode = mode;
        _lastFinalLabel = result.finalLabel;
        std::string labelStr = (mode == Mode::DIGITS && result.finalLabel >= 0 && result.finalLabel <= 9)
            ? std::string(1, '0' + result.finalLabel) : std::to_string(result.finalLabel);
        std::ostringstream topRowStream;
        topRowStream << "Top class: " << labelStr << ", Confidence: " << std::fixed << std::setprecision(2) << result.finalConfidence << ", Model: " << result.finalModelName;
        lblTopRow.setTitle(topRowStream.str());
        static const char* modelKeys[] = {"KNN", "NaiveBayes", "MiniMLP", "AStar", "RuleEngine"};
        for (unsigned index = 0; index < _modelCount; ++index) {
            auto it = result.modelComparison.find(modelKeys[index]);
            if (it != result.modelComparison.end()) {
                std::ostringstream modelStream;
                modelStream << _modelDisplayNames[index] << ": " << it->second.label << ", Confidence: " << std::fixed << std::setprecision(2) << it->second.confidence;
                _modelLabels[index]->setTitle(modelStream.str());
            }
        }
        lblFeedback.setTitle("Is the prediction OK?");
        return true;
    }
    if (button == &btnClear) {
        _hasPrediction = false;
        clearPredictionLabels();
        return true;
    }
    if (button == &btnCorrect) {
        if (!_hasPrediction) {
            lblFeedback.setTitle("Predict first.");
            return true;
        }
        _engine.updateModel(_lastMode, _currentImage, _lastFinalLabel);
        _hasPrediction = false;
        lblFeedback.setTitle("Thanks for feedback!");
        return true;
    }
    if (button == &btnIncorrect) {
        if (!_hasPrediction) {
            lblFeedback.setTitle("Predict first.");
            return true;
        }
        _hasPrediction = false;
        lblFeedback.setTitle("Thanks for feedback!");
        return true;
    }
    if (button == &btnMetrics) {
        Mode displayMode = _hasPrediction ? _lastMode : Mode::DIGITS;
        static const char* metricsModelKeys[] = {"KNN", "NaiveBayes", "MiniMLP", "AStar"};
        static const char* metricsDisplayNames[] = {"KNN", "N. Bayes", "MLP", "A*"};
        gui::Label* metricsLabels[] = {&lblMetricsKNN, &lblMetricsNaiveBayes, &lblMetricsMLP, &lblMetricsAStar};
        for (unsigned modelIndex = 0; modelIndex < 4; ++modelIndex) {
            std::shared_ptr<ConfusionMatrix> confusionMatrix = _engine.getMetrics(displayMode, metricsModelKeys[modelIndex]);
            if (confusionMatrix) {
                std::ostringstream accuracyStream;
                accuracyStream << std::fixed << std::setprecision(2) << confusionMatrix->getAccuracy();
                metricsLabels[modelIndex]->setTitle(std::string(metricsDisplayNames[modelIndex]) + " accuracy " + accuracyStream.str());
            } else {
                metricsLabels[modelIndex]->setTitle(std::string(metricsDisplayNames[modelIndex]) + " (no data)");
            }
        }
        lblMetricsTitle.setTitle("Confusion matrices");
        return true;
    }
    return false;
}

bool MainView::handleUserEvent(td::UINT4 eventID, const td::Variant& userParam) {
    (void)eventID;
    (void)userParam;
    return false;
}
