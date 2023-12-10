import pandas as pd
import streamlit as st
import altair as alt

@st.cache_data
def trialrun():

    df2 = pd.read_csv("trail_data.csv", sep = ',')

    return df2
   
df2 = trialrun()
st.title("Airplane bird strikes analysis in the US")
page = st.sidebar.selectbox("Select a page ",["Select","Filtered by Phase of Flight", "Filtered by Airports"])

def phase_flight(df2):
    selected_option = st.sidebar.selectbox("Select the phase of flight you want to get some graphs of: ", df2['New Phase of Flight'].unique())

    data = df2[df2["New Phase of Flight"] == selected_option]

    counts = data.groupby('Strike part').size().reset_index(name='count')
    counts['percentage'] = ((counts['count'] / counts['count'].sum()) * 100).round(2)

    gradient_to = "#ed0000"
    gradient_from = "#fcc5c5"

    alt_chart = (alt.Chart(counts , title = f"Bird strike percentage on airplane part during {selected_option}").mark_bar()
                .encode(x = 'Strike part:N',
                        y = 'percentage:Q',
                        color=alt.Color('percentage:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())

    st.altair_chart(alt_chart, use_container_width= True)

    counts2 = data.groupby('Airport').size().reset_index(name='count')
    counts2 = counts2.sort_values(by = 'count', ascending = False)
    counts2 = counts2.head(10)

    gradient_to = "#ed0000"
    gradient_from = "#fcc5c5"

    alt_chart2 = (alt.Chart(counts2 , title = f"Bird strikes in top 10 airports during {selected_option}").mark_bar()
                .encode(x = 'Airport:N',
                        y = 'count:Q',
                        color=alt.Color('count:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())

    st.altair_chart(alt_chart2, use_container_width= True)

if page == "Filtered by Phase of Flight":
    phase_flight(df2)