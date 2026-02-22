#pragma once
#include <gui/View.h>
#include <gui/Button.h>
#include <gui/Label.h>
#include <gui/VerticalLayout.h>
#include <gui/HorizontalLayout.h>
#include "ai/Engine.h"
#include "data/DataManager.h"
#include "data/Image.h"
#include "data/Mode.h"
#include <string>

class MainView : public gui::View
{
protected:
    gui::Button btnDigits;
    gui::Button btnShapes;
    gui::Button btnSymbols;
    gui::Label lblPredictionTitle;
    gui::Label lblTopRow;
    gui::Label lblComparisonTitle;
    gui::Label lblKNN;
    gui::Label lblNaiveBayes;
    gui::Label lblMLP;
    gui::Label lblAStar;
    gui::Label lblRuleFallback;

    gui::Button btnLoadImage;
    gui::Button btnClear;
    gui::Button btnMetrics;
    gui::Label lblFeedback;
    gui::Button btnCorrect;
    gui::Button btnIncorrect;

    gui::View predictionFrameView;
    gui::View feedbackFrameView;
    gui::View metricsFrameView;
    gui::Label lblMetricsTitle;
    gui::Label lblMetricsKNN;
    gui::Label lblMetricsNaiveBayes;
    gui::Label lblMetricsMLP;
    gui::Label lblMetricsAStar;

    gui::HorizontalLayout modeBarLayout;
    gui::VerticalLayout predictionPanel;
    gui::VerticalLayout feedbackVerticalLayout;
    gui::HorizontalLayout feedbackButtonsLayout;
    gui::VerticalLayout rightLayout;
    gui::VerticalLayout metricsPanelLayout;
    gui::HorizontalLayout footerLayout;
    gui::VerticalLayout mainLayout;

    static const unsigned _modelCount = 5;
    gui::Label* _modelLabels[_modelCount];
    void clearPredictionLabels();

    std::string _currentImagePath;
    Image _currentImage{28, 28};
    Engine _engine;

    bool _hasPrediction = false;
    Mode _lastMode = Mode::DIGITS;
    int _lastFinalLabel = -1;

public:
    MainView();
    bool onClick(gui::Button* button) override;
    bool handleUserEvent(td::UINT4 eventID, const td::Variant& userParam) override;
};
