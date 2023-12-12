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
page = st.sidebar.selectbox("Select a page ",["Home","Overall","Filtered by State", "Filtered by Airports","Filtered by Phase of Flight"])
gradient_to = "#ed0000"
gradient_from = "#fcc5c5"

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

#  Idea for next page is to have a line chart to represent the overall data like the strike count over the years,
#  can have an option to filter the years by decade. it can also have the cost of repairs, the cost due to an 
#  action taken.
#  Can merge State and Airport if possible
#  filters like which bird species cost the most damage or strike count or impact in which state etc

def overall():
    years = st.sidebar.selectbox("Select a decade",["All years","1990s", "2000s", "2010s", "2020s"])
    years_range = {"All years":(1990,2024), "1990s": (1990,2000), "2000s": (2000,2010), "2010s": (2010,2020), "2020s":(2020,2024)}
    target_decade_from, target_decade_to = years_range[years]
    filtered_df = df2[df2['Incident Year'].between(target_decade_from, target_decade_to)]
    yearly_counts = filtered_df['Incident Year'].value_counts().reset_index(name = 'count')
    yearly_counts.columns = ['Incident Year', 'count']

    year, cost = st.tabs(["Yearly strikes", "Yearly cost of repairs"])

    alt_chart = (alt.Chart(yearly_counts , title = f"Line chart for yearly strikes").mark_area()
                .encode(x = 'Incident Year:N',
                        y = 'count:Q'
                        # color=alt.Color('count:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())
    
    with year:
            st.altair_chart(alt_chart, use_container_width= True)

    cost_counts = filtered_df.groupby('Incident Year')['Cost Repairs'].sum().reset_index()
    cost_counts['Cost Repairs'] = cost_counts['Cost Repairs']/ 1_000_000.0
    # cost_counts = df2['Cost Repairs'].value_counts().reset_index(name = 'count')

    alt_chart2 = (alt.Chart(cost_counts , title = f"Line chart for Yearly cost of repairs").mark_area()
                .encode(x = 'Incident Year:O',
                        y = 'Cost Repairs:Q'
                        # color=alt.Color('count:Q', scale=alt.Scale(range=[gradient_from, gradient_to]))
                        )
                        .interactive())
    
    with cost:
        st.altair_chart(alt_chart2, use_container_width= True)

def home():
    st.write('''In perhaps the most famous bird strike incident, a US Airways jet lost power in both engines
              after striking geese after takeoff from LaGuardia Airport in 2009. The captain, Chesley “Sully” 
             Sullenberger III, brought the plane down in the Hudson River in what became known as the “Miracle
              on the Hudson.” All 155 people onboard survived.''')
    st.image('sully.jpeg', caption='Hudson river airplane emergency landing')
    st.write('''The FAA agency says that, across the world, more than 300 people were killed because of wildlife strikes
                and nearly 300 planes were destroyed between 1988 and 2021. 
                “Bird strikes are a hazard to aviation,” said Hassan Shahidi, president and CEO of the Flight Safety Foundation.
                  “And it happens frequently, and not just to commercial airplanes, but to all sorts of aircraft."''')
    st.image('Sully~2.jpg', caption='Hudson river airplane emergency landing')
    st.write("Source: https://www.washingtonpost.com/travel/2023/04/25/bird-strike-plane-american-airlines/")


if page == "Filtered by Phase of Flight":
    phase_flight(df2)

elif page == "Filtered by Airports":
    airport(df2)

elif page == "Filtered by State":
    state(df2)

elif page == "Overall":
    overall()

elif page == "Home":
    home()
