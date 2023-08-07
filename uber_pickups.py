import streamlit as st
import pandas as pd
import numpy as np
import os

# Get the data directory
current_directory = os.getcwd()
relative_path = 'data/uber-raw-data-sep14.csv'
absolute_path = os.path.join(current_directory, relative_path)

DATE_COLUMN = 'date/time'
DATA_URL = (absolute_path)

@st.cache_data
def load_data(nrows):


    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

st.set_page_config(layout="wide")
st.title('Uber Pickups in NYC')

data_slider = st.slider("Number of datapoints used:", 0, 1000000, 10000)
data_load_state = st.text('Loading data...')
data = load_data(data_slider)
data_load_state.text(f"Done! You're now viewing results of {data_slider} trips!")



if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(data, width=1400)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23, default 17
hour_to_filter = st.slider('Pick the hour of the day:', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)