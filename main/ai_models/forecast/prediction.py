import pickle

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from xgboost import XGBRegressor
import pandas as pd
from skforecast.model_selection import bayesian_search_forecaster
import pickle
from skforecast.model_selection import backtesting_forecaster
# from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error as mae

def forecast(kpi_name, nb_steps, data):

	with open(f'model-{kpi_name}.pkl', 'rb') as file:
		forecaster = pickle.load(file)

	df = pd.DataFrame(data)
	df["Timestamp"] = df["timestamp"]
	df["KPI_Value"] = df["kpi_value"]
	df.drop(columns = ["timestamp", "kpi_value"])
	df["Timestamp"] = pd.to_datetime(df["Timestamp"])
	df = df.sort_values(by="Timestamp")
	df.set_index("Timestamp", inplace=True)
	df = df.asfreq("T")
	df.interpolate(method="linear")

	df['day_of_week'] = df.index.dayofweek
	df['day'] = df.index.day
	df['month'] = df.index.month
	df['hour'] = df.index.hour
	df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
	df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

	metric, predictions = backtesting_forecaster(
					forecaster		 = forecaster,
					y				 = df["KPI_Value"],
					exog	  =  df[["day_of_week", "month","hour", "day", "day_sin", "day_cos"]],
					steps			  = nb_steps,
					metric			 = 'mean_absolute_error',
					initial_train_size = None,
					refit			  = False,
					n_jobs			 = 'auto',
					verbose			= False, # Change to False to see less information
					show_progress	  = True
				)
	return predictions

data = [
    {'timestamp': '2021-01-01 00:00:00', 'kpi_value': 100},
    {'timestamp': '2021-01-01 01:00:00', 'kpi_value': 105},
    {'timestamp': '2021-01-01 02:00:00', 'kpi_value': 98},
    {'timestamp': '2021-01-01 03:00:00', 'kpi_value': 110},
    {'timestamp': '2021-01-01 04:00:00', 'kpi_value': 95},
    {'timestamp': '2021-01-01 05:00:00', 'kpi_value': 102},
    {'timestamp': '2021-01-01 06:00:00', 'kpi_value': 108},
    {'timestamp': '2021-01-01 07:00:00', 'kpi_value': 97},
    {'timestamp': '2021-01-01 08:00:00', 'kpi_value': 103},
    {'timestamp': '2021-01-01 09:00:00', 'kpi_value': 99},
    {'timestamp': '2021-01-01 10:00:00', 'kpi_value': 107},
    {'timestamp': '2021-01-01 11:00:00', 'kpi_value': 96},
    {'timestamp': '2021-01-01 12:00:00', 'kpi_value': 104},
    {'timestamp': '2021-01-01 13:00:00', 'kpi_value': 101},
    {'timestamp': '2021-01-01 14:00:00', 'kpi_value': 109},
    {'timestamp': '2021-01-01 15:00:00', 'kpi_value': 93},
    {'timestamp': '2021-01-01 16:00:00', 'kpi_value': 106},
    {'timestamp': '2021-01-01 17:00:00', 'kpi_value': 100},
    {'timestamp': '2021-01-01 18:00:00', 'kpi_value': 105},
    {'timestamp': '2021-01-01 19:00:00', 'kpi_value': 98},
    {'timestamp': '2021-01-01 20:00:00', 'kpi_value': 110},
    {'timestamp': '2021-01-01 21:00:00', 'kpi_value': 95},
    {'timestamp': '2021-01-01 22:00:00', 'kpi_value': 102},
    {'timestamp': '2021-01-01 23:00:00', 'kpi_value': 108},
    {'timestamp': '2021-01-02 00:00:00', 'kpi_value': 97},
    {'timestamp': '2021-01-02 01:00:00', 'kpi_value': 103},
    {'timestamp': '2021-01-02 02:00:00', 'kpi_value': 99},
    {'timestamp': '2021-01-02 03:00:00', 'kpi_value': 107},
    {'timestamp': '2021-01-02 04:00:00', 'kpi_value': 96},
    {'timestamp': '2021-01-02 05:00:00', 'kpi_value': 104},
    {'timestamp': '2021-01-02 06:00:00', 'kpi_value': 101},
    {'timestamp': '2021-01-02 07:00:00', 'kpi_value': 109},
    {'timestamp': '2021-01-02 08:00:00', 'kpi_value': 93},
    {'timestamp': '2021-01-02 09:00:00', 'kpi_value': 106},
    {'timestamp': '2021-01-02 10:00:00', 'kpi_value': 100},
    {'timestamp': '2021-01-02 11:00:00', 'kpi_value': 105},
    {'timestamp': '2021-01-02 12:00:00', 'kpi_value': 98},
    {'timestamp': '2021-01-02 13:00:00', 'kpi_value': 110},
    {'timestamp': '2021-01-02 14:00:00', 'kpi_value': 95},
    {'timestamp': '2021-01-02 15:00:00', 'kpi_value': 102},
    {'timestamp': '2021-01-02 16:00:00', 'kpi_value': 108},
    {'timestamp': '2021-01-02 17:00:00', 'kpi_value': 97},
    {'timestamp': '2021-01-02 18:00:00', 'kpi_value': 103},
    {'timestamp': '2021-01-02 19:00:00', 'kpi_value': 99},
    {'timestamp': '2021-01-02 20:00:00', 'kpi_value': 107},
    {'timestamp': '2021-01-02 21:00:00', 'kpi_value': 96},
    {'timestamp': '2021-01-02 22:00:00', 'kpi_value': 104},
    {'timestamp': '2021-01-02 23:00:00', 'kpi_value': 101},
    {'timestamp': '2021-01-03 00:00:00', 'kpi_value': 109},
    {'timestamp': '2021-01-03 01:00:00', 'kpi_value': 93},
    {'timestamp': '2021-01-03 02:00:00', 'kpi_value': 106}
]

transformed_data = {
    'timestamp': [entry['timestamp'] for entry in data],
    'kpi_value': [entry['kpi_value'] for entry in data]
}

df = pd.DataFrame(transformed_data)

print(forecast('Stamping Press Efficiency', 10, df))