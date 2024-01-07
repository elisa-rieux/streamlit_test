import streamlit as st
from collections import namedtuple
import math
import pandas as pd
import numpy as np
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image       # this package is used to put images within streamlit
import matplotlib.pyplot as plt

from api_connection import get_data_from_api       # keep this commented if not using it otherwise brakes the app
from api_connection import get_data_forecast

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# List of cities
cities = ["Barcelona", "Madrid", "Paris", "New York", "Tokyo", "London", "Berlin"]

option = st.sidebar.selectbox(
    "Make a choice",
    ("City localisation", "Weather analysis", "Weather forecast")
)

# Widget in order to select a city
selected_city = st.selectbox("Chose a city", cities)

# Data
weather_data = get_data_from_api(selected_city)
weather_forecast = get_data_forecast(selected_city)

if option == "City localisation":
    # City localisation
    if st.checkbox("Show city localisation"):
        st.map(pd.DataFrame({'lat': [weather_data['coord']['lat']], 'lon': [weather_data['coord']['lon']]}))

if option == "Weather analysis":
    ### Weather analysis
    st.header("Weather analysis")
    # Row A
    a1, a2  = st.columns(2)
    #a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
    a1.metric("Temperature", f"{weather_data['main']['temp']} °C")
    a2.metric("Humidity", f"{weather_data['main']['humidity']}%")

    # Row B
    a4, a5 = st.columns(2)
    a4.metric("Pressure", f"{weather_data['main']['pressure']} hPa")
    a5.metric("Weather", weather_data['weather'][0]['description'].capitalize())

    if st.checkbox("Show wind details"):
        st.write(f"Wind speed: {weather_data['wind']['speed']} m/s")
        st.write(f"Wind direction: {weather_data['wind']['deg']}°")

    ## Zoom on the temperature
    st.header("Zoom on temperature")
    def temp_comp():
        # Data for the chart
        temps = [weather_data['main']['temp_min'], weather_data['main']['temp'], weather_data['main']['temp_max']]
        labels = ['Temp Min', 'Current Temp', 'Temp Max']
        fig, ax = plt.subplots()
        bars = ax.bar(labels, temps, color=['blue', 'green', 'red'])  # Changing colors
        # Adding titles and legends
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Min, Current, and Max Temperatures of the day')
        ax.set_xticklabels(labels)
        # Displaying the values on the bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom')  # Display the value above each bar
            # Display the chart in Streamlit
        st.pyplot(fig)

    temp_comp()

if option == "Weather forecast":
    ### Weather forecast

    def plot_temperature_trend(data):
        # Convert timestamps to timezone-naive datetime objects
        timestamps = [pd.to_datetime(forecast['dt_txt']).tz_localize(None) for forecast in data['list']]
        temps = [forecast['main']['temp'] for forecast in data['list']]
        # Create the plot
        plt.figure(figsize=(10, 6))  # You can adjust the plot size as needed
        plt.plot(timestamps, temps)
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Trend during the next days')
        plt.xticks(rotation=45)  # Rotate date labels for better readability
        st.pyplot(plt.gcf())

    def display_forecast_table(data):
        # Extracting and transforming the data into a DataFrame
        forecasts = data['list'][:9]  # Limiting to the next 24h
        forecast_df = pd.DataFrame([{
            'Date': pd.to_datetime(forecast['dt_txt']),
            'Temperature': forecast['main']['temp'],
            'Description': forecast['weather'][0]['description']
        } for forecast in forecasts])
        # Displaying the table in Streamlit with a title
        st.table(forecast_df)

    st.header("24h Weather Forecast")
    display_forecast_table(weather_forecast)

    st.header("Weather Forecast graph for the next few days")
    plot_temperature_trend(weather_forecast)