import pandas as pd
import streamlit as st
import altair as alt
import datetime as dt

@st.cache_data
def trialrun():

    df2 = pd.read_csv("trail_data.csv", sep = ',')

    return df2
   
df2 = trialrun()
st.title("Airplane bird strikes analysis in the US")
page = st.sidebar.selectbox("Select a page ",["Select","Filtered by Phase of Flight", "Filtered by Airports","Filtered by State"])

def phase_flight(df2):
    # bar = st.sidebar.radio("",["Airplane part striked","Top 10 airports"])
    part, top = st.tabs(["Airplane part striked","Top 10 airports"])
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

    with part:
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

    with top:
        st.altair_chart(alt_chart2, use_container_width= True)


def airport(df2):
    selected_option = st.sidebar.selectbox("Select the airport you want to get some graphs of: ", df2['Airport'].unique())
    
    data = df2[df2["Airport"] == selected_option]

    counts = data.groupby('Strike part').size().reset_index(name='count')
    val = len(data)
    counts['percentage'] = ((counts['count'] / counts['count'].sum()) * 100).round(2)
    st.write(f"Bird strikes at {selected_option} airport are {val}")
    gradient_to = "#ed0000"
    gradient_from = "#fcc5c5"
    part, day = st.tabs(["Airplane part striked", "Time of the day"])
    alt_chart = (alt.Chart(counts , title = f"Bird strike percentage on airplane part during {selected_option}").mark_bar()
                .encode(x = 'Strike part:N',
                        y = 'percentage:Q',
                        color=alt.Color('percentage:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())
    with part:
        st.altair_chart(alt_chart, use_container_width= True)
    
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M',errors='coerce').dt.time

    # Add a new column 'time_day' with default value
    data['time_day'] = ""

    # Update 'time_day' based on the time range
    for i, r in data[['Time']].iterrows():
        if not pd.isnull(r['Time']):
            if dt.time(3, 0) <= r['Time'] < dt.time(12, 0):
                data.at[i, 'time_day'] = "Morning"
            elif dt.time(12, 0) <= r['Time'] < dt.time(16, 0):
                data.at[i, 'time_day'] = "Afternoon"
            elif dt.time(16, 0) <= r['Time'] < dt.time(20, 0):
                data.at[i, 'time_day'] = "Evening"
            elif dt.time(20, 0) <= r['Time'] < dt.time(3, 0):
                data.at[i, 'time_day'] = "Night"
            else:
                data.at[i, 'time_day'] = "Night"
    data_filtered = data[data['time_day'] != '']
    counts2 = data_filtered.groupby('time_day').size().reset_index(name='count')

    counts2['percentage'] = ((counts2['count'] / counts2['count'].sum()) * 100).round(2)

    # alt_chart2 = (alt.Chart(counts2 , title = f"Bird strike percentage on airplane part during {selected_option}").mark_bar()
    #             .encode(x = 'time_day:N',
    #                     y = 'count:Q',
    #                     color=alt.Color('percentage:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
    #                     )
    #                     .interactive())
    
    # st.altair_chart(alt_chart2, use_container_width= True)
    custom_colors = {'Night': '#3b82a2', 'Morning': '#efcb77', 'Afternoon': '#b74d38', 'Evening': '#aad675'}

    chart3 = alt.Chart(counts2).mark_arc().encode(
    theta = 'count:Q',
    color= alt.Color('time_day:N', scale=alt.Scale(range=list(custom_colors.values()))),
    ).properties(
    width=400,
    height=400, 
    title='Distribution of Time of Day'
    )
    with day:
        st.altair_chart(chart3, use_container_width=True)

def state(df2):
    selected_option = st.sidebar.selectbox("Select a state: ", df2['State'].unique())
    data = df2[df2["State"] == selected_option]
    val = len(data)
    st.write(f"Total {val} number of airplane bird strikes reported in the state of {selected_option} ")
    
    map, bar = st.tabs(["Map distribution of reported strikes", "Bird species involved in the strike"])
    with map:
        st.map(data, latitude= 'latitude', longitude= ' longitude')

    counts = data.groupby("Species").size().reset_index(name = "count")
    gradient_to = "#ed0000"
    gradient_from = "#fcc5c5"
    counts = counts.sort_values(by = 'count', ascending = False)

    counts = counts.head(10)
    alt_chart = (alt.Chart(counts , title = f"Top 10 bird strike species in {selected_option}").mark_bar()
                .encode(x = 'Species:N',
                        y = 'count:Q',
                        color=alt.Color('count:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())
    
    with bar:
        st.altair_chart(alt_chart, use_container_width = True)



if page == "Filtered by Phase of Flight":
    phase_flight(df2)

elif page == "Filtered by Airports":
    airport(df2)

elif page == "Filtered by State":
    state(df2)
