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
    globalDataframe.LandAverageTemperature.bfill(inplace=True)

    globalDataframe.drop(columns=["Date"], inplace=True)

    return globalDataframe

globalDataframe = loadGlobalData()

st.title("Motivation and Data Analysis")
st.write("La previsione dell'aumento delle temperature è un tema di grande interesse per la situazione globale attuale. Con lo sviluppo degli algoritmi di Machine Learning e nello specifico di Deep Learning è stato possibile creare modelli tali da predirre con una precisione accettabile le serie temporali.")
st.write("Lo scopo di questo progetto è quello di analizzare un dataset di temperature raccolte nell'arco di tempo che va dal 1850 al 2015, in modo da progettare un buon predittore capace di fornire informazioni sull'aumento delle temperature globali nel corso dei prossimi anni.")

st.subheader("Raw dataset")

st.dataframe(globalDataframe)
st.write("Il dataset in questione è composto da una serie temporale che giorno per giorno indica:")
st.markdown("- **Land Average Temperature:** la temperatura media globale in un dato giorno.")
st.markdown("- **Land Average Temperature Uncertainty:** l'incertezza delle misurazioni effettuate.")
st.markdown("- **Land Max Temperature:** la temperatura massima in un dato giorno.")
st.markdown("- **Land Min Temperature:** la temperatura minima in un dato giorno.")
st.markdown("- **Land And Ocean Average Temperature:** la temperatura media globale in un dato giorno, considerando anche la temperatura degli oceani.")

st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)

st.subheader("Key points: autocorrelation and seasonality")

st.write("La chiave per le predizioni è la correlazione tra le temperature tra giorni più o meno vicini. Di conseguenza può essere utile notare quanto i nostri dati siano **autocorrelati**, ovvero quanto le temperature siano statisticamente correlate tra di esse al trascorrere dei giorni.")

figure = sgt.plot_acf(globalDataframe.LandAverageTemperature , lags= 60, zero =True , title = "Autocorrelation of climate change")
st.pyplot(figure)

st.write("È chiaro che abbiamo picchi di correlazione positiva ogni 12 mesi, in cui effettivamente una predizione può trarre vantaggio del fatto che si stanno misurando dei dati nello stesso periodo stagionale. A tal proposito, il dataset in questione si presta chiaramente a un'analisi di **seasonality**, in quanto i dati stessi rispettano intrinsecamente parametri di ripetizione stagionale.")

s_dec_additive = seasonal_decompose(globalDataframe.LandAverageTemperature[-100:], model = "additive", period=24)

fig = s_dec_additive.plot()
fig.set_size_inches(20, 20)
st.pyplot(fig)

st.write("Si nota quindi nuovamente il pattern di ciclicità, stavolta nella decomposizione di **trend** e **seasonality**.")