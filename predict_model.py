import pandas as pd
import yfinance as yf
from yahoo_earnings_calendar import YahooEarningsCalendar
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd
import numpy as np
import math
import datetime
import json

def predict_model():
    # Fetch the data
    ticker = 'BBYB.JK'

    # last_week_date = datetime.today() - timedelta(days = 7)
    # last_week_date_format = datetime.strptime(last_week_date, '%Y-%m:%d')
    # csv_data = yf.download(ticker, '2017-01-01', last_week_date_format)
    # csv_data.head()

    # current_date = datetime.today()
    # current_date_format = datetime.strptime(current_date, '%Y-%m:%d')
    # csv_data = yf.download(ticker, '2017-01-01', last_week_date_format)
    # csv_data.head()

    current_date = datetime.date.today()
    csv_data = yf.download(ticker, '2017-01-01', '2023-01-18')
    csv_data.head()

    # Create the data
    csv_data['TradeDate']=csv_data.index
    
    # Plot the stock prices
    # csv_data.plot(x='TradeDate', y='Close', kind='line', figsize=(20,6), rot=20)

    FullData=csv_data[['Close']].values
    # print(FullData[-15:])
    
    # Feature Scaling for fast training of neural networks
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    
    # Choosing between Standardization or normalization
    sc=MinMaxScaler()
    
    DataScaler = sc.fit(FullData)
    X=DataScaler.transform(FullData)

    # Making predictions on test data
    Last10DaysPrices = FullData[-22:-7]
    real_seven_days = FullData[-7:]

    # Reshaping the data to (-1, 1) because its a single entry
    Last10DaysPrices=Last10DaysPrices.reshape(-1, 1)
    
    # Scaling the data on the same level on which model was trained
    X_test=DataScaler.transform(Last10DaysPrices)

    NumberofSamples=1
    TimeSteps=X_test.shape[0]
    NumberofFeatures=X_test.shape[1]
    # Reshaping the data as 3D input
    X_test=X_test.reshape(NumberofSamples,TimeSteps,NumberofFeatures)

    regressor = keras.models.load_model('/content/drive/MyDrive/bbybjk_training_model.h5')
    
    # Generating the predictions for next 5 days
    Next5DaysPrice = regressor.predict(X_test)

    # Generating the prices in original scale
    Next5DaysPrice = DataScaler.inverse_transform(Next5DaysPrice)

    print(Next5DaysPrice)
    print(real_seven_days)

    mse_loss = MeanSquaredError()

    # Making predictions on test data
    Last10DaysPrices=FullData[-15:]
                    #np.array([1376.2, 1371.75,1387.15,1370.5 ,1344.95, 1312.05, 1316.65, 1339.45, 1339.7 ,1340.85])
    
    # Reshaping the data to (-1,1 )because its a single entry
    Last10DaysPrices=Last10DaysPrices.reshape(-1, 1)
    
    # Scaling the data on the same level on which model was trained
    X_test=DataScaler.transform(Last10DaysPrices)
    
    NumberofSamples=1
    TimeSteps=X_test.shape[0]
    NumberofFeatures=X_test.shape[1]
    # Reshaping the data as 3D input
    X_test=X_test.reshape(NumberofSamples,TimeSteps,NumberofFeatures)

    regressor = keras.models.load_model('/content/drive/MyDrive/bbybjk_training_model.h5')
    
    # Generating the predictions for next 5 days
    Next5DaysPrice = regressor.predict(X_test)

    # Generating the prices in original scale
    Next5DaysPrice = DataScaler.inverse_transform(Next5DaysPrice)

    json_str = json.dumps({
        "prediksi": Next5DaysPrice.tolist()
    })

    return json_str