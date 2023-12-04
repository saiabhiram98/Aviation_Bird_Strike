import pandas as pd
import streamlit as st

@st.cache_data

def trialrun():
    data = pd.read_csv('STRIKE_REPORTS.csv', sep=',', dtype=str)

    st.write(data.head(10))
    st.write("Hello World")

trialrun()