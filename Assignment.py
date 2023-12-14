import pandas as pd
import streamlit as st
import altair as alt
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
@st.cache_data
def trialrun():

    df2 = pd.read_csv("trail_data.csv", sep = ',')

    return df2
   
df2 = trialrun()

page = st.sidebar.selectbox("Select a page ",["Home","Comprehensive insights","Filtered by State", "Filtered by Airports"])
gradient_to = "#3498db"
gradient_from = "#1f77b4"
color_2 = "#3c9e50"

def airport(df2):
    selected_option = st.sidebar.selectbox("Select the airport you want to get some graphs of: ", df2['Airport'].unique())
    st.title(f"Airplane bird strikes analysis filtered by Airport of {selected_option}")
    data = df2[df2["Airport"] == selected_option]

    counts = data.groupby('Strike part').size().reset_index(name='count')
    val = len(data)
    counts['percentage'] = ((counts['count'] / counts['count'].sum()) * 100).round(2)
    st.write(f"Bird strikes at {selected_option} airport are {val}")

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

    state_dict = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts',
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }

    selected_option = st.sidebar.selectbox("Select a state: ", state_dict.values())
    st.title(f"Airplane bird strikes filtered by State of {selected_option}")

    def get_key_by_value(state_dict, selected_option):
        for key, value in state_dict.items():
            if value == selected_option:
                return key
        return None

    data = df2[df2["State"] ==  get_key_by_value(state_dict,selected_option)]
    val = len(data)
    st.write(f"Total **{val}** number of airplane bird strikes reported in the state of {selected_option} ")
    
    map, bar = st.tabs(["Map distribution of reported strikes", "Bird species involved in the strike"])
    with map:
        st.map(data, latitude= 'latitude', longitude= ' longitude')

    counts = data.groupby("Species").size().reset_index(name = "count")

    counts = counts.sort_values(by = 'count', ascending = False)

    counts = counts.head(10)
    counts = counts.sort_values(by = 'count', ascending = True)
    counts['index'] = range(len(counts))
    alt_chart = (alt.Chart(counts , title = f"Top 10 bird strike species in {selected_option}").mark_bar()
                .encode(x = alt.X('Species:O',axis=alt.Axis(titleColor='#344037')),
                        y = alt.Y('count:Q', title= "Count", axis=alt.Axis(titleColor='#344037'), sort= 'ascending'),
                        color=alt.value(gradient_to)
                        ).configure_axis(
                        labelColor='#344037') 
                        .interactive())
    
    with bar:
        st.altair_chart(alt_chart, use_container_width = True)

#  Idea for next page is to have a line chart to represent the overall data like the strike count over the years,
#  can have an option to filter the years by decade. it can also have the cost of repairs, the cost due to an 
#  action taken.
#  Can merge State and Airport if possible
#  filters like which bird species cost the most damage or strike count or impact in which state etc

def overall():

    selected_year = st.sidebar.slider('Select a range of Years', min_value=df2['Incident Year'].min(), max_value=df2['Incident Year'].max(), value=(df2['Incident Year'].min(), df2['Incident Year'].max()))
    filtered_df = df2[df2['Incident Year'].between(selected_year[0], selected_year[1])]    
    yearly_counts = filtered_df.groupby('Incident Year').size().reset_index(name='count')   

    year, cost, top = st.tabs(["Yearly strikes", "Yearly cost of repairs", "Top 10 airports"])

    alt_chart = alt.Chart(yearly_counts , title = f"Line chart for yearly strikes and comparison with phase of flight between {selected_year[0]} to {selected_year[1]}"
                          ).mark_area().encode(
                          alt.X('Incident Year:N'), alt.Y('count:Q'),
                           color =alt.value(gradient_to),
                           tooltip=['Incident Year:N', 'count:Q']).interactive()


    selected_option2 = st.sidebar.selectbox("Select the phase of the flight for comparison : ", df2['New Phase of Flight'].unique())
    data = filtered_df[filtered_df["New Phase of Flight"] == selected_option2] 
    counts = data.groupby('Incident Year').size().reset_index(name='count with phase')
    alt_chart_ = alt.Chart(counts).mark_area().encode(
                        x = 'Incident Year:N',
                        y = 'count with phase:Q',
                        color=alt.value(gradient_from),
                        tooltip=['Incident Year:N', 'count with phase:Q']
                        )
    combined = alt_chart+alt_chart_

    with year:
            st.altair_chart(combined, use_container_width= True)


    
    cost_counts = filtered_df.groupby('Incident Year')['Cost Repairs'].sum().reset_index()
    cost_counts['Cost Repairs'] = cost_counts['Cost Repairs']/ 1_000_000.0

    alt_chart2 = (alt.Chart(cost_counts , title = f"Line chart for Yearly cost of repairs between {selected_year[0]} to {selected_year[1]}").mark_area()
                .encode(x = 'Incident Year:O',
                        y = alt.Y('Cost Repairs:Q', title = "Cost of repairs in million"),
                        color=alt.value(gradient_to)
                        ).interactive())
    
    data = filtered_df[filtered_df["New Phase of Flight"] == selected_option2] 
    counts_cost = data.groupby('Incident Year')['Cost Repairs'].sum().reset_index()
    counts_cost['Cost Repairs'] = counts_cost['Cost Repairs']/ 1_000_000.0

    alt_chart2_ = alt.Chart(counts_cost).mark_area().encode(
                        x = 'Incident Year:N',
                        y = 'Cost Repairs:Q',
                        color=alt.value(gradient_from),
                        tooltip=['Incident Year:N', 'Cost Repairs:Q']
                        )
    
    combined_chart2 = alt_chart2 + alt_chart2_
    with cost:
        st.altair_chart(combined_chart2, use_container_width= True)


    counts2 = filtered_df.groupby('Airport').size().reset_index(name='count')
    counts2 = counts2.sort_values(by = 'count', ascending = False)
    counts2 = counts2[counts2["Airport"] != 'UNKNOWN']
    counts2 = counts2.head(10)
    
    airport_list = []
    for i,j in counts2.iterrows():
        airport_list.append(j[0])
  
    alt_chart3 = (alt.Chart(counts2 , title = f"Bird strikes in top 10 airports between {selected_year[0]} to {selected_year[1]}").mark_bar()
            .encode(x = 'Airport:N',
                    y = 'count:Q',
                    color=alt.value(gradient_to)
                    ).interactive())

    data = filtered_df[filtered_df["New Phase of Flight"] == selected_option2] 
    counts_airport = data.groupby('Airport').size().reset_index(name = 'count')
    counts_airport = counts_airport.sort_values(by = 'count', ascending = False)
    counts_airport = counts_airport[counts_airport["Airport"] != 'UNKNOWN']
    counts_airport_final = pd.DataFrame([])

    for i, j in counts_airport.iterrows():
        if j['Airport'] in airport_list:
            counts_airport_final = pd.concat([counts_airport_final, pd.DataFrame({'Airport': [j['Airport']], 'count': [j['count']]})])

    alt_chart3_ = alt.Chart(counts_airport_final).mark_bar().encode(
                        x = 'Airport:N',
                        y = 'count:Q',
                        color=alt.value(gradient_from),
                        tooltip=['Airport:N', 'count:Q']
                        )
    
    combined_chart3 = alt_chart3 + alt_chart3_
    with top:
        st.altair_chart(combined_chart3, use_container_width= True)

    

def home():
    st.title("Airplane bird strikes analysis in the US")
    
    st.write('''Airplane bird strikes refer to incidents where birds collide with aircraft during flight or during takeoff and landing. These collisions can pose a significant risk to aviation safety, potentially causing damage to aircraft engines, wings, and other critical components. To mitigate this risk, airports and aviation authorities employ various measures, such as wildlife management programs and the development of bird strike reporting systems, to enhance safety for both passengers and crew.''')
    st.write('''This app provides a comprehensive visualization of bird strike data for over 33 years, offering insights into yearly strike patterns, state-wise distribution, and other critical analyses. By leveraging data from the past three decades, users can better understand the dynamics of bird strikes, aiding in the development of strategies to mitigate the risks associated with this aviation hazard.''')
    
    st.write('''In perhaps the most famous bird strike incident, a US Airways jet lost power in both engines after striking geese after takeoff from LaGuardia Airport in 2009. The captain, Chesley “Sully” Sullenberger III, brought the plane down in the Hudson River in what became known as the “Miracle on the Hudson.” All 155 people onboard survived.''')
    
    st.image('sully.jpeg', caption='Real photo of Hudson river airplane emergency landing',width=650)
    st.write('''The FAA agency says that, across the world, more than 300 people were killed because of wildlife strikes
                and nearly 300 planes were destroyed between 1988 and 2021. 
                “Bird strikes are a hazard to aviation,” said Hassan Shahidi, president and CEO of the Flight Safety Foundation.
                  “And it happens frequently, and not just to commercial airplanes, but to all sorts of aircraft."''')
    st.image('Sully.jpg', caption='Sully: Tom Hanks Movie based on the Hundson river incident',width=650)
    st.write("Source: https://www.washingtonpost.com/travel/2023/04/25/bird-strike-plane-american-airlines/")


if page == "Filtered by Phase of Flight":
    phase_flight(df2)

elif page == "Filtered by Airports":
    airport(df2)

elif page == "Filtered by State":
    state(df2)

elif page == "Comprehensive insights":
    overall()

elif page == "Home":
    home()
 