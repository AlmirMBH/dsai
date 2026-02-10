import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

import config

REGRESSORS = config.FORECAST_REGRESSORS
REVPAR_REGRESSORS = config.FORECAST_REVPAR_REGRESSORS
CALENDAR_COUNT = config.LSTM_CALENDAR_COUNT
INPUT_DAYS = config.LSTM_INPUT_DAYS
MAX_HORIZON = config.LSTM_MAX_HORIZON
DEFAULT_EPOCHS = config.LSTM_DEFAULT_EPOCHS


def _calendar_features(dates: np.ndarray) -> np.ndarray:
    dt = pd.to_datetime(dates)
    dow = dt.dayofweek.values
    week_of_year = dt.isocalendar().week.astype(float).values
    dow_sin = np.sin(2 * np.pi * dow / 7)
    dow_cos = np.cos(2 * np.pi * dow / 7)
    week_sin = np.sin(2 * np.pi * week_of_year / 52)
    week_cos = np.cos(2 * np.pi * week_of_year / 52)
    is_weekend = (dow >= 5).astype(np.float64)
    return np.column_stack([dow_sin, dow_cos, week_sin, week_cos, is_weekend])


def _build_features(df: pd.DataFrame, target: str, regressor_list: list, scaler_target=None, use_log_target: bool = False):
    raw_target = df[target].values.reshape(-1, 1)
    target_values = np.log1p(raw_target) if use_log_target else raw_target
    if scaler_target is None:
        scaler_target = StandardScaler()
        target_scaled = scaler_target.fit_transform(target_values)
    else:
        target_scaled = scaler_target.transform(target_values)
    regressor_values = df[regressor_list].values
    calendar_values = _calendar_features(df["date"].values)
    features = np.column_stack([target_scaled.ravel(), regressor_values, calendar_values])
    return features, scaler_target


def _multihorizon_supervised(data: np.ndarray, n_lag: int, n_out: int) -> tuple[np.ndarray, np.ndarray]:
    n = len(data)
    if n < n_lag + n_out:
        return np.array([]).reshape(0, n_lag, data.shape[1]), np.array([]).reshape(0, n_out)
    x_list = []
    y_list = []
    for i in range(n_lag, n - n_out + 1):
        x_list.append(data[i - n_lag : i])
        y_list.append(data[i : i + n_out, 0])
    return np.array(x_list), np.array(y_list)


def _inverse_target(scaled_values: np.ndarray, scaler_target: StandardScaler, use_log_target: bool) -> np.ndarray:
    raw = scaler_target.inverse_transform(scaled_values.reshape(-1, 1)).ravel()
    return np.expm1(raw) if use_log_target else raw


def lstm_full_predictions(
    train: pd.DataFrame,
    test: pd.DataFrame,
    target: str,
    epochs: int = DEFAULT_EPOCHS,
) -> tuple[pd.Series, pd.Series]:
    train = train.sort_values("date").reset_index(drop=True)
    test = test.sort_values("date").reset_index(drop=True)
    horizon = min(len(test), len(train) - INPUT_DAYS)
    if horizon < 1:
        raise ValueError(f"Train too short for input_days={INPUT_DAYS} and test length {len(test)}")
    use_log_target = target == "revpar"
    regressor_list = REVPAR_REGRESSORS if target == "revpar" else REGRESSORS
    n_features = 1 + len(regressor_list) + CALENDAR_COUNT
    values, scaler_target = _build_features(train, target, regressor_list, use_log_target=use_log_target)
    if len(values) < INPUT_DAYS + horizon:
        raise ValueError(f"Train too short for input_days={INPUT_DAYS} and horizon={horizon}")

    X_train, y_train = _multihorizon_supervised(values, INPUT_DAYS, horizon)
    if len(X_train) == 0:
        raise ValueError("No multi-horizon samples")

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(INPUT_DAYS, n_features)),
        tf.keras.layers.LSTM(48, activation="relu"),
        tf.keras.layers.Dense(horizon),
    ])
    model.compile(optimizer="adam", loss=tf.keras.losses.Huber(), metrics=["mae"])
    early_stop = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True, monitor="val_loss")
    model.fit(
        X_train, y_train,
        epochs=epochs, batch_size=8,
        validation_split=0.2, callbacks=[early_stop], verbose=0,
    )

    in_sample_preds = []
    for start in range(INPUT_DAYS, len(values)):
        window = values[start - INPUT_DAYS : start].reshape(1, INPUT_DAYS, n_features)
        pred_h = model.predict(window, verbose=0)[0]
        in_sample_preds.append(pred_h[0])
    in_sample = _inverse_target(np.array(in_sample_preds), scaler_target, use_log_target)
    in_sample_dates = train["date"].iloc[INPUT_DAYS:].values
    lead_dates = train["date"].iloc[:INPUT_DAYS].values
    lead_values = train[target].iloc[:INPUT_DAYS].values

    last_window = values[-INPUT_DAYS:].reshape(1, INPUT_DAYS, n_features)
    forecast_h = model.predict(last_window, verbose=0)[0]
    forecast_values = _inverse_target(forecast_h, scaler_target, use_log_target)
    forecast_dates = test["date"].values[:horizon]
    forecast_values = forecast_values[:horizon]

    pred_dates = np.concatenate([lead_dates, in_sample_dates, forecast_dates])
    pred_values = np.concatenate([lead_values, in_sample, forecast_values])
    return pd.Series(pred_dates), pd.Series(pred_values)
