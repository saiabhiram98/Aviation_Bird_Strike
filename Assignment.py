import pandas as pd
import streamlit as st
import altair as alt

@st.cache_data
def trialrun():
    st.title("Aviation Bird Strike Analysis")
    data = pd.read_csv('STRIKE_REPORTS.csv', sep=',', dtype=str)
    data2 = pd.read_csv('STRIKE_REPORTS.csv', sep=',', dtype=str)
    # st.write(data.head(10))
    # st.write("Hello World")

    grouped_data = data2.groupby("Airport")
 
    count_data = pd.DataFrame(grouped_data.size())  
    count_data = count_data.reset_index()
    # st.write(count_data.columns)
    # st.write(count_data.head(10))
    count_data.columns = ["Airport","Incident count"]
    count_data = count_data.sort_values(by = "Incident count", ascending= False)
    # st.write(count_data)
    
    count_data = count_data.head(10)
    count_data_filtered = count_data[count_data["Airport"] != "UNKNOWN"]
    # st.write(count_data.columns)
    chart = alt.Chart(count_data_filtered).mark_bar().encode(
    x="Airport",
    y='Incident count'
    ).properties(
    title='Incident Count by Airport'   
    )
    st.altair_chart(chart, use_container_width= True)

trialrun()