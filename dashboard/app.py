import streamlit as st
import pandas as pd
import numpy as np 

data = pd.read_csv(r'D:\aqi_forecast_arima\AQI_forecast_arima\data\historical_pm25_weather.csv')

st.line_chart(data=data)

