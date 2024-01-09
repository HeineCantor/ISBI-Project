import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import math
import pydeck as pdk

st.set_page_config(page_title="Global Land Temperature Prediction")

css='''
<style>
    section.main > div {max-width:75rem}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>Global Land Temperature Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>-Letizia Arena, Leonardo Ferrara, Carmine Palmese-</h3>", unsafe_allow_html=True)

temperatureChoiceToIndex = {
    "**Absolute**" : 0,
    "**Relative to city**" : 1,
    "**Threshold**" : 2,
}

def latLongConvert(x : str):
    sgn = +1
    if x[-1] == 'S' or x[-1] == 'W':
        sgn = -1

    return float(x[:-1]) * sgn

def temperatureToColor(temperature, minTemp, maxTemp):
    if(math.isnan(temperature) or temperature == ""):
        return (0, 0, 0)
    redAmount = np.ceil((temperature-minTemp)/(maxTemp-minTemp) *255)
    blueAmount = 255 - redAmount
    return (redAmount, 0, blueAmount, 140)

def relativeTemperatureToColor(temperature, datafame, city):
    cityDF = datafame[datafame["City"] == city]

    minRelativeTemperature = cityDF.AverageTemperature.min()
    maxRelativeTemperature = cityDF.AverageTemperature.max()

    return temperatureToColor(temperature, minRelativeTemperature, maxRelativeTemperature)

@st.cache_data
def loadData():
    cityDataframe = pd.read_csv("./Datasets/converted.csv")
    cityDataframe.rename(columns={"dt":"Date", "Latitude":"latitude", "Longitude":"longitude"}, inplace=True)
    cityDataframe.Date = pd.to_datetime(cityDataframe.Date)
    cityDataframe.drop(cityDataframe[(cityDataframe.Date.dt.month != 1) | (cityDataframe.Date.dt.day != 1)].index, inplace=True)

    cityDataframe.set_index(cityDataframe["Date"], inplace=True)

    minTemperature = cityDataframe.AverageTemperature.min()
    maxTemperature = cityDataframe.AverageTemperature.max()

    cityDataframe["AbsoluteColor"] = [temperatureToColor(x, minTemperature, maxTemperature) for x in cityDataframe.AverageTemperature.tolist()]
    cityDataframe["RelativeColor"] = [relativeTemperatureToColor(x[0], cityDataframe, x[1]) for x in zip(cityDataframe.AverageTemperature.tolist(), cityDataframe.City.tolist())]

    return cityDataframe

cityDataframe = loadData()

minTemperature = cityDataframe.AverageTemperature.min()
maxTemperature = cityDataframe.AverageTemperature.max()

maxYear = cityDataframe.Date.max().year
minYear = 1900 #cityDataframe.Date.min().year

yearToDisplay = st.slider('Year of interest', minYear, maxYear, minYear) 

filteredDataframe = cityDataframe[cityDataframe.Date.dt.year == yearToDisplay]

mapColumns = st.columns([4,1])
colorMode = 0

temperatureThreshold = 0

with mapColumns[1]:
    temperatureColorChoice = st.radio(
        "***Temperature colors:***", 
        ["**Absolute**", "**Relative to city**", "**Threshold**"],
        captions = ["Based on global max and min temperatures in all years.", "Relative to max and min temperature of a specific city.", "Cold/Hot threshold specified below."],
        )
    
    colorMode = temperatureChoiceToIndex[temperatureColorChoice]

    if(colorMode == 2):
        temperatureThreshold = st.slider('Temperature threshold', minTemperature, maxTemperature, 0.0) 

with mapColumns[0]:
    if(colorMode == 0):
        st.pydeck_chart(pdk.Deck(
                map_style=None,
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        filteredDataframe,
                        get_position=['longitude', 'latitude'],
                        auto_highlight=True,
                        get_radius=300000,
                        get_fill_color='AbsoluteColor',
                        pickable=True)
                ]
            )
        )
    elif(colorMode == 1):
        st.pydeck_chart(pdk.Deck(
                map_style=None,
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        filteredDataframe,
                        get_position=['longitude', 'latitude'],
                        auto_highlight=True,
                        get_radius=300000,
                        get_fill_color='RelativeColor',
                        pickable=True)
                ]
            )
        )
    elif(colorMode == 2):
            st.pydeck_chart(pdk.Deck(
                map_style=None,
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        filteredDataframe,
                        get_position=['longitude', 'latitude'],
                        auto_highlight=True,
                        get_radius=300000,
                        get_fill_color=f'[AverageTemperature >= {temperatureThreshold} ? 255 : 0, 0, AverageTemperature >= {temperatureThreshold} ? 0 : 255, 140]',
                        pickable=True)
                ]
            )
        )

st.subheader("Average temperature chart by country (moving average on 30 years)")

listOfDisplayableCountries = ["Italy", "France", "Germany", "Spain", "United Kingdom"]

cityOptions = st.multiselect(
    'Cities to display',
    listOfDisplayableCountries,
    listOfDisplayableCountries
)

chartData = pd.DataFrame()

chartData["Date"] = cityDataframe[(cityDataframe.Country == "Italy")].Date
for country in cityOptions:
    chartData[f"{country} Temperature"] = cityDataframe[cityDataframe.Country == country].AverageTemperature.rolling(window=30).mean()
chartData.drop(chartData[chartData.Date.dt.year < 1900].index, inplace=True)
st.line_chart(chartData, x="Date")

st.subheader("Maximal recorded values")

statsDataframe = cityDataframe.loc[cityDataframe['AverageTemperature'].idxmax()].iloc[:,:-2]
st.write(statsDataframe)

st.subheader("Minimal recorded values")

statsDataframe = cityDataframe.loc[cityDataframe['AverageTemperature'].idxmin()].iloc[:,:-2]
st.write(statsDataframe)

#st.write(chartData)
