import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import preprocessor,helper
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally' , 'OverAll Analysis' , 'Country wise analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df , selected_year , selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("OVERALL TALLY")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("MedalTally in "+ str(selected_year))
    if(selected_year == 'Overall' and selected_country != 'Overall'):
        st.title("MedalTally for " + str(selected_country))
    if(selected_year!='Overall' and selected_country!='Overall'):
        st.title(str(selected_country) + " Over All performance in " + str(selected_year))
    st.table(medal_tally)


if user_menu == 'OverAll Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("TOP STATS")
    col1 , col2 , col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athletes")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations)



if user_menu == 'Country wise analysis':

    st.sidebar.title('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country ' , country_list)

    country_df = helper.yearwise_medal_tally(df , selected_country)
    fig = px.line(country_df , x = "Year"  , y = "Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excells in the following sports")
    pt= helper.country_event_heatmap(df , selected_country)
    fig , ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

