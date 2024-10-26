import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent


def predict(data: list[dict], kpi: str):
    test_data = pd.DataFrame(data)
    test_data['Timestamp'] = pd.to_datetime(test_data['Timestamp'])
    # test_data = test_data[~test_data.index.duplicated(keep='first')]
    # remove duplicate timestamps
    test_data = test_data.drop_duplicates(subset='Timestamp', keep='first')

    test_data.set_index('Timestamp', inplace=True)
    test_data.sort_index(inplace=True)
    test_data = test_data.asfreq('min')
    test_data['KPI_Value'] = test_data['KPI_Value'].interpolate(method='linear')

    test_data['day_of_week'] = test_data.index.dayofweek
    test_data['day'] = test_data.index.day
    test_data['month'] = test_data.index.month
    test_data['hour'] = test_data.index.hour
    test_data['day_sin'] = np.sin(2 * np.pi * test_data['day_of_week'] / 7)
    test_data['day_cos'] = np.cos(2 * np.pi * test_data['day_of_week'] / 7)
    test_data.reset_index(inplace=True, drop=True)

    test_data['lag_1'] = test_data['KPI_Value'].shift(1)
    test_data['lag_2'] = test_data['KPI_Value'].shift(2)
    test_data['lag_3'] = test_data['KPI_Value'].shift(3)

    test_data['KPI_Value_mean'] = test_data['KPI_Value'].rolling(window=5).mean()
    test_data['KPI_Value_std'] = test_data['KPI_Value'].rolling(window=5).std()
    test_data['KPI_Value_max'] = test_data['KPI_Value'].rolling(window=5).max()
    test_data['KPI_Value_min'] = test_data['KPI_Value'].rolling(window=5).min()

    test_data.dropna(inplace=True)

    if not len(test_data):
        raise Exception("No enough data to make a prediction")

    model: xgb.XGBClassifier = joblib.load(os.path.join(BASE_DIR,  f'models/{kpi}_model.pkl'))
    pred = model.predict(test_data)
    return bool(pred[-1])
