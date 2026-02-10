import pandas as pd
from prophet import Prophet

import config

REGRESSORS = config.FORECAST_REGRESSORS
LOGISTIC_MARGIN = config.PROPHET_LOGISTIC_MARGIN
CHANGEPOINT_PRIOR_SCALE = config.PROPHET_CHANGEPOINT_PRIOR_SCALE
SEASONALITY_PRIOR_SCALE = config.PROPHET_SEASONALITY_PRIOR_SCALE


def prophet_full_predictions(train: pd.DataFrame, test: pd.DataFrame, target: str) -> tuple[pd.Series, pd.Series]:
    df_train = train[["date", target] + REGRESSORS].copy()
    df_train = df_train.rename(columns={"date": "ds", target: "y"})
    df_train["ds"] = pd.to_datetime(df_train["ds"]).dt.normalize()

    is_revpar = target == "revpar"
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=CHANGEPOINT_PRIOR_SCALE,
        seasonality_prior_scale=SEASONALITY_PRIOR_SCALE,
        seasonality_mode="multiplicative" if is_revpar else "additive",
        growth="logistic" if target == "demand" else "linear",
    )
    demand_cap = None
    demand_floor = None
    if target == "demand":
        train_demand = df_train["y"].values
        demand_min = float(train_demand.min())
        demand_max = float(train_demand.max())
        margin = max(1, (demand_max - demand_min) * LOGISTIC_MARGIN) if demand_max > demand_min else 1
        demand_floor = max(0, demand_min - margin)
        demand_cap = demand_max + margin
        df_train["cap"] = demand_cap
        df_train["floor"] = demand_floor
    for r in REGRESSORS:
        model.add_regressor(r)
    model.fit(df_train)

    full = pd.concat([train, test], ignore_index=True).sort_values("date").drop_duplicates(subset=["date"])
    future = full[["date"] + REGRESSORS].copy()
    future = future.rename(columns={"date": "ds"})
    future["ds"] = pd.to_datetime(future["ds"]).dt.normalize()
    if target == "demand":
        future["cap"] = demand_cap
        future["floor"] = demand_floor
    forecast = model.predict(future)
    return pd.Series(forecast["ds"].values), pd.Series(forecast["yhat"].values)
