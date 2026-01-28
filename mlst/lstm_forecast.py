import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def series_to_supervised(data, number_of_input_lags=1, number_of_output_steps=1, dropnan=True):
    number_of_variables = 1 if type(data) is list else data.shape[1]
    data_frame = pd.DataFrame(data)
    column_list, column_names = [], []
    for lag in range(number_of_input_lags, 0, -1):
        column_list.append(data_frame.shift(lag))
        column_names += [("var%d(t-%d)" % (var_idx + 1, lag)) for var_idx in range(number_of_variables)]
    for step in range(0, number_of_output_steps):
        column_list.append(data_frame.shift(-step))
        if step == 0:
            column_names += [("var%d(t)" % (var_idx + 1)) for var_idx in range(number_of_variables)]
        else:
            column_names += [("var%d(t+%d)" % (var_idx + 1, step)) for var_idx in range(number_of_variables)]
    aggregated = pd.concat(column_list, axis=1)
    aggregated.columns = column_names
    if dropnan:
        aggregated.dropna(inplace=True)
    return aggregated

N_FEATURES = 3

def build_rnn_model(keras_layer, units, time_steps, n_features=N_FEATURES):
    inputs = tf.keras.layers.Input(shape=(time_steps, n_features))
    rnn_out = keras_layer(units, activation="relu")(inputs)
    outputs = tf.keras.layers.Dense(1)(rnn_out)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model


def _build_features(df_historical, target_column, scaler=None):
    target = df_historical[target_column].values.reshape(-1, 1)
    if scaler is None:
        scaler = MinMaxScaler(feature_range=(0, 1))
        target_scaled = scaler.fit_transform(target)
    else:
        target_scaled = scaler.transform(target)
    month_norm = df_historical["month"].values / 12.0
    dow_norm = df_historical["date"].dt.dayofweek.values / 6.0
    return np.column_stack([target_scaled.flatten(), month_norm, dow_norm]), scaler


def prepare_sequences_full(df_historical, target_column, time_steps=5):
    min_length = time_steps + 2
    if len(df_historical) < min_length:
        raise ValueError(
            f"Series has {len(df_historical)} points; LSTM needs at least {min_length} (time_steps={time_steps} + 2)."
        )
    values, scaler = _build_features(df_historical, target_column)
    reframed = series_to_supervised(values, time_steps, 1)
    reframed_values = reframed.values
    if len(reframed_values) == 0:
        raise ValueError("No sequences after reframing; need more data.")
    n_input_cols = time_steps * N_FEATURES
    train_inputs = reframed_values[:, :n_input_cols].reshape((len(reframed_values), time_steps, N_FEATURES))
    train_targets = reframed_values[:, -3]
    last_date = pd.Timestamp(df_historical["date"].iloc[-1])
    return train_inputs, train_targets, scaler, last_date


def predict_future_steps(model, scaler, df_historical, target_column, time_steps, last_date, periods):
    values, _ = _build_features(df_historical, target_column, scaler=scaler)
    last_window = values[-time_steps:]
    forecast_scaled = []
    for i in range(periods):
        x = last_window.reshape(1, time_steps, N_FEATURES)
        pred = model.predict(x, verbose=0)
        forecast_scaled.append(pred[0, 0])
        next_date = last_date + pd.Timedelta(days=i + 1)
        new_row = [pred[0, 0], next_date.month / 12.0, next_date.dayofweek / 6.0]
        last_window = np.vstack([last_window[1:], new_row])
    forecast_orig = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq="D")
    return forecast_dates, forecast_orig


MAX_TRAIN_STEPS = 256
DEFAULT_EPOCHS = 5
DEFAULT_TIME_STEPS = 5


def train_forecast_lstm(df_historical, periods, epochs=DEFAULT_EPOCHS, time_steps=DEFAULT_TIME_STEPS):
    train_x_d, train_y_d, scaler_d, last_date_d = prepare_sequences_full(
        df_historical, "demand", time_steps=time_steps
    )
    train_x_r, train_y_r, scaler_r, last_date_r = prepare_sequences_full(
        df_historical, "revpar", time_steps=time_steps
    )
    model_demand = build_rnn_model(tf.keras.layers.LSTM, 100, time_steps)
    model_revpar = build_rnn_model(tf.keras.layers.LSTM, 100, time_steps)
    steps_d = min(MAX_TRAIN_STEPS, max(1, len(train_x_d) // 8))
    steps_r = min(MAX_TRAIN_STEPS, max(1, len(train_x_r) // 8))
    model_demand.fit(train_x_d, train_y_d, epochs=epochs, batch_size=8, steps_per_epoch=steps_d, verbose=0)
    model_revpar.fit(train_x_r, train_y_r, epochs=epochs, batch_size=8, steps_per_epoch=steps_r, verbose=0)
    forecast_dates_d, forecast_demand = predict_future_steps(
        model_demand, scaler_d, df_historical, "demand", time_steps, last_date_d, periods
    )
    forecast_dates_r, forecast_revpar = predict_future_steps(
        model_revpar, scaler_r, df_historical, "revpar", time_steps, last_date_r, periods
    )
    models_scalers = (model_demand, model_revpar, scaler_d, scaler_r)
    return models_scalers, forecast_dates_d, forecast_demand, forecast_dates_r, forecast_revpar


def predict_forecast_lstm(model_demand, model_revpar, scaler_d, scaler_r, df_historical, periods, time_steps=DEFAULT_TIME_STEPS):
    last_date = pd.Timestamp(df_historical["date"].iloc[-1])
    forecast_dates_d, forecast_demand = predict_future_steps(
        model_demand, scaler_d, df_historical, "demand", time_steps, last_date, periods
    )
    forecast_dates_r, forecast_revpar = predict_future_steps(
        model_revpar, scaler_r, df_historical, "revpar", time_steps, last_date, periods
    )
    return forecast_dates_d, forecast_demand, forecast_dates_r, forecast_revpar
