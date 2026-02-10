import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date

from data_ingestion import get_data
from dataset_aggregation_by_day import preprocess
from data_ingestion import add_lagged_regressors, train_test_split, standardize_regressors
from forecast_prophet import prophet_full_predictions
from forecast_lstm import lstm_full_predictions

DEFAULT_TEST_DAYS = 30
_REVPAR_LABEL = ". RevPAR: "


def _plot_metric(ax, train_dates, train_values, test_dates, test_values, pred_dates, pred_values, split_date, y_label, title=None):
    ax.plot(train_dates, train_values, color="C0", label="Train Data", solid_capstyle="round")
    ax.plot(test_dates, test_values, color="C1", label="Test Data", solid_capstyle="round")
    ax.plot(pred_dates, pred_values, color="C2", linestyle="--", label="Predictions", solid_capstyle="round")
    ax.axvline(split_date, color="red", linestyle="--", alpha=0.9)
    ax.set_xlabel("Date (daily)")
    ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)
    ax.legend()
    ax.figure.autofmt_xdate()


def _mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    return np.abs(actual - predicted).mean()


def _rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    return np.sqrt(((actual - predicted) ** 2).mean())


def _smape(actual: np.ndarray, predicted: np.ndarray) -> float:
    num = np.abs(actual - predicted)
    denom = (np.abs(actual) + np.abs(predicted)) / 2.0
    mask = denom > 0
    return (100.0 * np.mean(num[mask] / denom[mask])) if np.any(mask) else 0.0


def _period_metrics(
    pred_dates: pd.Series,
    pred_values: pd.Series,
    period_df: pd.DataFrame,
    target: str,
) -> tuple[float | None, float | None, float | None]:
    period_dates = pd.to_datetime(period_df["date"]).dt.normalize()
    pred_dates_n = pd.to_datetime(pred_dates).dt.normalize()
    merged = pd.DataFrame({"date": period_dates, "actual": period_df[target].values})
    pred_df = pd.DataFrame({"date": pred_dates_n, "yhat": pred_values.values})
    merged = merged.merge(pred_df, on="date", how="inner")
    if len(merged) == 0:
        return None, None, None
    actual = merged["actual"].values
    yhat = merged["yhat"].values
    return _mae(actual, yhat), _rmse(actual, yhat), _smape(actual, yhat)


def render_forecast_compare():
    st.subheader("Forecast Compare")

    bookings, events, weather, _, bus_schedules = get_data()
    if len(bookings) == 0 or len(events) == 0:
        st.warning("No datasets available. Generate datasets first.")
        return

    df = preprocess(bookings, events, weather, bus_schedules)
    today = pd.Timestamp(date.today())
    df = df[df["date"] <= today].copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df = add_lagged_regressors(df)

    test_days = st.slider("Test period (days)", 7, 90, DEFAULT_TEST_DAYS, key="compare_test_days")
    min_rows = 7 + test_days + 1
    if len(df) < min_rows:
        st.warning("Need at least {} days; got {}.".format(min_rows, len(df)))
        return
    train, test, split_date = train_test_split(df, test_days=test_days)
    train = train.iloc[7:].reset_index(drop=True)
    train_std, test_std = standardize_regressors(train, test)

    with st.spinner("Training Prophet…"):
        prophet_demand_dates, prophet_demand_values = prophet_full_predictions(train_std, test_std, "demand")
        prophet_revpar_dates, prophet_revpar_values = prophet_full_predictions(train_std, test_std, "revpar")
    with st.spinner("Training LSTM…"):
        lstm_demand_dates, lstm_demand_values = lstm_full_predictions(train_std, test_std, "demand")
        lstm_revpar_dates, lstm_revpar_values = lstm_full_predictions(train_std, test_std, "revpar")

    train_dates = train["date"].values
    test_dates = test["date"].values
    all_demand = np.concatenate([train["demand"].values, test["demand"].values, prophet_demand_values.values, lstm_demand_values.values])
    all_revpar = np.concatenate([train["revpar"].values, test["revpar"].values, prophet_revpar_values.values, lstm_revpar_values.values])
    demand_axis_min, demand_axis_max = np.nanmin(all_demand), np.nanmax(all_demand)
    revpar_axis_min, revpar_axis_max = np.nanmin(all_revpar), np.nanmax(all_revpar)
    if demand_axis_max <= demand_axis_min:
        demand_axis_min, demand_axis_max = demand_axis_min - 1, demand_axis_max + 1
    if revpar_axis_max <= revpar_axis_min:
        revpar_axis_min, revpar_axis_max = revpar_axis_min - 1, revpar_axis_max + 1
    date_axis_min = min(train_dates.min(), test_dates.min())
    date_axis_max = max(train_dates.max(), test_dates.max())

    st.markdown("#### Prophet")
    fig_demand, ax_demand = plt.subplots(figsize=(10, 4))
    _plot_metric(ax_demand, train_dates, train["demand"].values, test_dates, test["demand"].values,
                prophet_demand_dates, prophet_demand_values, split_date, "Demand", "Demand – Prophet")
    ax_demand.set_ylim(demand_axis_min, demand_axis_max)
    ax_demand.set_xlim(date_axis_min, date_axis_max)
    st.pyplot(fig_demand)
    plt.close(fig_demand)
    fig_revpar, ax_revpar = plt.subplots(figsize=(10, 4))
    _plot_metric(ax_revpar, train_dates, train["revpar"].values, test_dates, test["revpar"].values,
                prophet_revpar_dates, prophet_revpar_values, split_date, "RevPAR", "RevPAR – Prophet")
    ax_revpar.set_ylim(revpar_axis_min, revpar_axis_max)
    ax_revpar.set_xlim(date_axis_min, date_axis_max)
    st.pyplot(fig_revpar)
    plt.close(fig_revpar)

    st.markdown("#### LSTM")
    fig_demand_lstm, ax_demand_lstm = plt.subplots(figsize=(10, 4))
    _plot_metric(ax_demand_lstm, train_dates, train["demand"].values, test_dates, test["demand"].values,
                lstm_demand_dates, lstm_demand_values, split_date, "Demand", "Demand – LSTM")
    ax_demand_lstm.set_ylim(demand_axis_min, demand_axis_max)
    ax_demand_lstm.set_xlim(date_axis_min, date_axis_max)
    st.pyplot(fig_demand_lstm)
    plt.close(fig_demand_lstm)
    fig_revpar_lstm, ax_revpar_lstm = plt.subplots(figsize=(10, 4))
    _plot_metric(ax_revpar_lstm, train_dates, train["revpar"].values, test_dates, test["revpar"].values,
                lstm_revpar_dates, lstm_revpar_values, split_date, "RevPAR", "RevPAR – LSTM")
    ax_revpar_lstm.set_ylim(revpar_axis_min, revpar_axis_max)
    ax_revpar_lstm.set_xlim(date_axis_min, date_axis_max)
    st.pyplot(fig_revpar_lstm)
    plt.close(fig_revpar_lstm)

    st.markdown("#### Metrics: Train, Test, Prediction (test period)")

    def format_metrics(mae, rmse, smape):
        return "MAE {:.2f}, RMSE {:.2f}, sMAPE {:.1f}%".format(mae or 0, rmse or 0, smape or 0)

    prophet_train_demand_mae, prophet_train_demand_rmse, prophet_train_demand_smape = _period_metrics(prophet_demand_dates, prophet_demand_values, train, "demand")
    prophet_train_revpar_mae, prophet_train_revpar_rmse, prophet_train_revpar_smape = _period_metrics(prophet_revpar_dates, prophet_revpar_values, train, "revpar")
    lstm_train_demand_mae, lstm_train_demand_rmse, lstm_train_demand_smape = _period_metrics(lstm_demand_dates, lstm_demand_values, train, "demand")
    lstm_train_revpar_mae, lstm_train_revpar_rmse, lstm_train_revpar_smape = _period_metrics(lstm_revpar_dates, lstm_revpar_values, train, "revpar")
    prophet_test_demand_mae, prophet_test_demand_rmse, prophet_test_demand_smape = _period_metrics(prophet_demand_dates, prophet_demand_values, test, "demand")
    prophet_test_revpar_mae, prophet_test_revpar_rmse, prophet_test_revpar_smape = _period_metrics(prophet_revpar_dates, prophet_revpar_values, test, "revpar")
    lstm_test_demand_mae, lstm_test_demand_rmse, lstm_test_demand_smape = _period_metrics(lstm_demand_dates, lstm_demand_values, test, "demand")
    lstm_test_revpar_mae, lstm_test_revpar_rmse, lstm_test_revpar_smape = _period_metrics(lstm_revpar_dates, lstm_revpar_values, test, "revpar")

    st.write("**Prophet**")
    st.write("- **Train (in-sample):** Demand: " + format_metrics(prophet_train_demand_mae, prophet_train_demand_rmse, prophet_train_demand_smape) + _REVPAR_LABEL + format_metrics(prophet_train_revpar_mae, prophet_train_revpar_rmse, prophet_train_revpar_smape) + ".")
    st.write("- **Test (prediction):** Demand: " + format_metrics(prophet_test_demand_mae, prophet_test_demand_rmse, prophet_test_demand_smape) + _REVPAR_LABEL + format_metrics(prophet_test_revpar_mae, prophet_test_revpar_rmse, prophet_test_revpar_smape) + ".")
    st.write("**LSTM**")
    st.write("- **Train (in-sample):** Demand: " + format_metrics(lstm_train_demand_mae, lstm_train_demand_rmse, lstm_train_demand_smape) + _REVPAR_LABEL + format_metrics(lstm_train_revpar_mae, lstm_train_revpar_rmse, lstm_train_revpar_smape) + ".")
    st.write("- **Test (prediction):** Demand: " + format_metrics(lstm_test_demand_mae, lstm_test_demand_rmse, lstm_test_demand_smape) + _REVPAR_LABEL + format_metrics(lstm_test_revpar_mae, lstm_test_revpar_rmse, lstm_test_revpar_smape) + ".")
    better_demand = "Prophet" if (prophet_test_demand_mae or np.inf) < (lstm_test_demand_mae or np.inf) else "LSTM"
    better_revpar = "Prophet" if (prophet_test_revpar_mae or np.inf) < (lstm_test_revpar_mae or np.inf) else "LSTM"
    st.write("**Conclusion:** For demand, {} has lower MAE; for RevPAR, {} has lower MAE.".format(better_demand, better_revpar))
