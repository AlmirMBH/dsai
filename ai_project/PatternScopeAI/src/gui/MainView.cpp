#include "MainView.h"
#include <gui/HorizontalLayout.h>
#include <gui/VerticalLayout.h>
#include <iomanip>
#include <sstream>

/**
 * Initialize all UI components and set up the layout based 
 * on the provided design references.
 */
MainView::MainView()
: lblPredictionTitle("Prediction Panel"),
  lblTopClass("Top Class: -"),
  lblConfidence("Confidence: 0.00"),
  lblAgentWarning("Agent: ready"),
  lblComparisonTitle("Model Comparison"),
  lblKNN("KNN: -"),
  lblNaiveBayes("Naive Bayes: -"),
  lblMLP("MLP: -"),
  lblAStarRulesTitle("A* & Rules"),
  lblAStarMatch("A* match: -"),
  lblRuleReason("Rule: -"),
  btnLoadImage("Load Image"),
  btnPredict("Predict Now"),
  btnClear("Clear"),
  btnTrain("Train"),
  btnConfusionMatrix("Confusion Matrix"),
  lblFeedback("Was this correct?"),
  btnCorrect("Yes"),
  btnWrong("No")
{
    gui::HorizontalLayout hLayout(2);
    
    // Left side: Large Drawing Canvas
    hLayout.append(canvas);

    // Right side: Data Display Panels
    gui::VerticalLayout rightLayout(4);
    
    // Prediction Summary Panel
    gui::VerticalLayout predictionPanel(4);
    predictionPanel.append(lblPredictionTitle);
    predictionPanel.append(lblTopClass);
    predictionPanel.append(lblConfidence);
    predictionPanel.append(lblAgentWarning);
    rightLayout.append(predictionPanel);

    // Individual Model Results
    gui::VerticalLayout comparisonPanel(4);
    comparisonPanel.append(lblComparisonTitle);
    comparisonPanel.append(lblKNN);
    comparisonPanel.append(lblNaiveBayes);
    comparisonPanel.append(lblMLP);
    rightLayout.append(comparisonPanel);

    // Template Matching & Heuristics
    gui::VerticalLayout rulesPanel(3);
    rulesPanel.append(lblAStarRulesTitle);
    rulesPanel.append(lblAStarMatch);
    rulesPanel.append(lblRuleReason);
    rightLayout.append(rulesPanel);

    // User Feedback for Active Learning
    gui::HorizontalLayout feedbackLayout(3);
    feedbackLayout.append(lblFeedback);
    feedbackLayout.append(btnCorrect);
    feedbackLayout.append(btnWrong);
    rightLayout.append(feedbackLayout);

    hLayout.append(rightLayout);

    // Final Stack: Panels on top, Nav buttons on bottom
    gui::VerticalLayout mainLayout(2);
    mainLayout.append(hLayout);
    
    gui::HorizontalLayout footerLayout(5);
    footerLayout.append(btnLoadImage);
    footerLayout.append(btnPredict);
    footerLayout.append(btnClear);
    footerLayout.append(btnTrain);
    footerLayout.append(btnConfusionMatrix);
    mainLayout.append(footerLayout);

    setLayout(&mainLayout);
}

/**
 * Switch the engine's recognition context (Digits, Shapes, or Symbols).
 */
void MainView::setMode(Mode mode) {
    currentMode = mode;
}

/**
 * Capture the canvas drawing and send it to the AI engine for analysis.
 */
void MainView::processDrawing() {
    Image image = canvas.getResizedImage();
    auto result = engine.predict(currentMode, image);
    updateUI(result);
}

/**
 * Update all labels in the GUI with the results from the recognition engine.
 */
void MainView::updateUI(const PredictionResult& result) {
    lblTopClass.setTitle("Top Class: " + std::to_string(result.finalLabel));
    
    std::stringstream stream;
    stream << "Confidence: " << std::fixed << std::setprecision(2) << result.finalConfidence;
    lblConfidence.setTitle(stream.str());

    lblAgentWarning.setTitle("Agent: " + result.finalModelName);

    // Map individual model results to their respective labels.
    if (result.modelComparison.count("KNN")) {
        lblKNN.setTitle("KNN: " + std::to_string(result.modelComparison.at("KNN").label));
    }
    if (result.modelComparison.count("NaiveBayes")) {
        lblNaiveBayes.setTitle("Naive Bayes: " + std::to_string(result.modelComparison.at("NaiveBayes").label));
    }
    if (result.modelComparison.count("MiniMLP")) {
        lblMLP.setTitle("MLP: " + std::to_string(result.modelComparison.at("MiniMLP").label));
    }
    if (result.modelComparison.count("AStar")) {
        lblAStarMatch.setTitle("A* match: " + std::to_string(result.modelComparison.at("AStar").label));
    }
}

/**
 * Handle button click events from the user.
 */
bool MainView::onClick(gui::Button* pBtn) {
    if (pBtn == &btnPredict) {
        processDrawing();
        return true;
    }
    if (pBtn == &btnClear) {
        canvas.clear();
        return true;
    }
    if (pBtn == &btnConfusionMatrix) {
        auto stats = engine.getMetrics(currentMode, "KNN");
        if (stats) {
            showAlert("Engine Stats", "Current Accuracy (KNN): " + std::to_string(stats->getAccuracy()));
        } else {
            showAlert("Engine Stats", "Stats not loaded. Please train first.");
        }
        return true;
    }
    if (pBtn == &btnCorrect) {
        lblFeedback.setTitle("Thanks for feedback!");
        return true;
    }
    return false;
}

/**
 * Handle custom events sent from child components (like the DrawingCanvas).
 */
bool MainView::handleUserEvent(td::UINT4 eventID, const td::Variant& userParam) {
    if (eventID == 1) { // User finished a mouse stroke
        processDrawing();
        return true;
    }
    return false;
}
