import streamlit as st
import pandas as pd
import numpy as np

# Load external CSS file
css_path = r'D:\aqi_forecast_arima\AQI_forecast_arima\dashboard\style.css'

# Read and apply the CSS file
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("AQI Forecasting Dashboard")

# Read main data from CSV
data = pd.read_csv(r'D:\aqi_forecast_arima\AQI_forecast_arima\data\historical_pm25_weather.csv')

# Clean the 'date' and 'hour' columns by stripping any extra spaces
data['date'] = data['date'].str.strip()
data['hour'] = data['hour'].str.strip()

# Combine 'date' and 'hour' to create a 'datetime' column
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['hour'], format='%d/%m/%Y %H:%M', errors='coerce')

# Set the datetime column as the index
data.set_index('datetime', inplace=True)

# Drop the original 'date' and 'hour' columns
data.drop(['date', 'hour'], axis=1, inplace=True)

# Read the forecast data (arima, sarima, sarimax forecasts)
forecast = pd.read_csv(r'D:\aqi_forecast_arima\AQI_forecast_arima\results\forecast_aqi.csv')

# Ensure the forecast data has the same datetime format as the main data
forecast['datetime'] = pd.to_datetime(forecast['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Read the AQI data
aqi_data = pd.read_csv(r'D:\aqi_forecast_arima\AQI_forecast_arima\results\aqi_data.csv')

# Ensure the AQI data datetime format is the same
aqi_data['datetime'] = pd.to_datetime(aqi_data['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Merge the AQI data with the forecast data on 'datetime' using an outer join
merged_aqi_forecast = pd.merge(aqi_data, forecast[['datetime', 'arima_forecast', 'sarima_forecast']], 
                               how='outer', on='datetime')

# Ensure datetime column exists and is in datetime format before setting it as index
if 'datetime' not in merged_aqi_forecast.columns:
    st.write("The 'datetime' column is missing in the merged data.")
else:
    merged_aqi_forecast['datetime'] = pd.to_datetime(merged_aqi_forecast['datetime'], errors='coerce')
    merged_aqi_forecast.set_index('datetime', inplace=True)

# Main content - Home section
st.subheader("Welcome to the AQI Forecasting Dashboard")
st.write("This dashboard allows you to view historical AQI data, along with ARIMA and SARIMA forecasts.")

# Create a selection box for the user to choose the graph
option = st.selectbox('Choose a graph to display:', ['AQI and Forecast', 'Temperature', 'Humidity'])

# Display the corresponding graph based on the selected option
if option == 'AQI and Forecast':
    st.subheader("AQI and Forecast Graph")
    st.write("This graph compares the AQI and its ARIMA and SARIMA forecasts.")
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)

    # Ensure that the necessary columns exist before plotting
    if 'aqi' in merged_aqi_forecast.columns and 'arima_forecast' in merged_aqi_forecast.columns and 'sarima_forecast' in merged_aqi_forecast.columns:
        st.line_chart(merged_aqi_forecast[['aqi', 'arima_forecast', 'sarima_forecast']])
    else:
        st.write("Missing necessary columns in the data for plotting.")

    st.markdown('</div>', unsafe_allow_html=True)

elif option == 'Temperature':
    st.subheader("Temperature Graph")
    st.write("This graph shows the temperature over time.")
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    
    # Ensure the 'temp' column exists before filtering
    if 'temp' in data.columns:
        filtered_data = data[data['temp'] != 0].copy()  # Avoid modifying original data
        st.line_chart(filtered_data['temp'])
    else:
        st.write("The 'temp' column is missing in the data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif option == 'Humidity':
    st.subheader("Humidity Graph")
    st.write("This graph shows the humidity levels over time.")
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    
    # Ensure the 'humidity' column exists before filtering
    if 'humidity' in data.columns:
        filtered_data = data[data['humidity'] != 0].copy()  # Avoid modifying original data
        st.line_chart(filtered_data['humidity'])
    else:
        st.write("The 'humidity' column is missing in the data.")
    st.markdown('</div>', unsafe_allow_html=True)
