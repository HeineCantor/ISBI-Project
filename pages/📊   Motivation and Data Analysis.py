import streamlit as st
import pandas as pd
import numpy as np

import statsmodels.tsa.stattools as sts
import statsmodels.graphics.tsaplots as sgt
from statsmodels.tsa.seasonal import seasonal_decompose

@st.cache_data
def loadGlobalData():
    globalDataframe = pd.read_csv("./Datasets/GlobalTemperatures.csv")
    globalDataframe.rename(columns={"dt":"Date", "Latitude":"latitude", "Longitude":"longitude"}, inplace=True)
    globalDataframe.Date = pd.to_datetime(globalDataframe.Date)
    globalDataframe.set_index(globalDataframe["Date"], inplace=True)
    globalDataframe = globalDataframe.iloc[1200:]
    globalDataframe.LandAverageTemperature.fillna(method="bfill", inplace=True)

    return globalDataframe

globalDataframe = loadGlobalData()

st.title("Motivation and Data Analysis")
st.text("blablabla")

st.subheader("Raw dataset")

st.dataframe(globalDataframe)
st.text("Description blabla")

st.subheader("Key points: autocorrelation and seasonality")

figure = sgt.plot_acf(globalDataframe.LandAverageTemperature , lags= 60, zero =True , title = "Autocorrelation of climate change")
st.pyplot(figure)

s_dec_additive = seasonal_decompose(globalDataframe.LandAverageTemperature[-100:], model = "additive", period=24)

fig = s_dec_additive.plot()
fig.set_size_inches(20, 20)
st.pyplot(fig)