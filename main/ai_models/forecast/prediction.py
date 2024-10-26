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
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent

def forecast(kpi_name, nb_steps, data):

	with open(os.path.join(BASE_DIR, f'model-{kpi_name}.pkl') , 'rb') as file:
		forecaster = pickle.load(file)

	df = pd.DataFrame(data)
	df["timestamp"] = pd.to_datetime(df["timestamp"])
	df = df.drop_duplicates(subset='timestamp', keep='first')
	df["Timestamp"] = df["timestamp"]
	df["KPI_Value"] = df["kpi_value"]
	df = df.drop(columns = ["timestamp", "kpi_value"])
	
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