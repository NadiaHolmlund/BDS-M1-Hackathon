import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from matplotlib.patches import ConnectionPatch
import plotly.express as px

data = pd.read_csv('https://raw.githubusercontent.com/NadiaHolmlund/BDS-M1-Hackathon/main/Data/attacks.csv', encoding='iso8859-1')

data.isna().sum()

data.drop(['Case Number', 'Name', 'Injury', 'Time', 'Investigator or Source', 'pdf', 'href formula', 'href', 'Case Number.1', 'Case Number.2', 'original order', 'Unnamed: 22', 'Unnamed: 23'], axis = 1, inplace = True)


# remove the space in the column name for better syntax and readability

data = data.rename(columns = {'Sex ':'Gender'})

# sort the unique values in column Gender into three categories: Female, Male and Unknown

data['Gender'] =  data['Gender'].replace(['M','M ', 'N'],'Male')
data['Gender'] =  data['Gender'].replace(['F'],'Female')
data['Gender'] =  data['Gender'].replace(['.','lli'],'Unknown')
data['Gender'] = data['Gender'].fillna('Unknown')


#from 1900 to 2018
sex_attacks = data.groupby('Gender')['Gender'].count()
sex_attacks = sex_attacks[(sex_attacks.index == 'Male') | (sex_attacks.index=='Female')|(sex_attacks.index=='Unknown')]

gender_fig = px.pie(sex_attacks, values=sex_attacks.values, names=sex_attacks.index)
gender_fig.update_layout(height=500, width=600)
gender_fig.show()

data = data[data['Year'] >= 1900]

# Test plot

byYear_attack = data.groupby('Year')['Date'].count().reset_index()
year_fig = px.line(byYear_attack,x='Year', y='Date', labels={'index':'','x':'Attack Count'}, title='Shark Attack by Year')
year_fig.update_traces(line_color='#149e14')
year_fig.show()

## Activities

len(data["Activity"].unique())

# Here making only 1 type, ALlType, so not 9 different provoked unprovked ETC.

data.loc[(data['Type'] == 'Boating') | (data['Type'] == 'Boatomg') | (data['Type'] == 'Boat') | (data['Type'] == 'Questionable') | (data['Type'] == 'Sea Disaster') | (data['Type'] == 'Invalid') | (data['Type'] == 'Provoked') | (data['Type'] == 'Unprovoked'), "Type"] = "AllType"
byType_count = data['Type'].value_counts().reset_index().rename(columns={'Type':'Count','index':'Type'})

# Total amount of attacks based on activity

prov_activity = data[data.Type == 'AllType'].groupby('Activity')['Activity'].count().sort_values(ascending=False)[:10]

activity_fig = px.bar(prov_activity, x=prov_activity.values, y=prov_activity.index, orientation='h', labels={'index':'','x':'Attack Count'},
            title = 'Shark Attacks by Activity', color='Activity', color_continuous_scale='Aggrnyl')
activity_fig.update_layout(height=600, width=900)
activity_fig.show()

# Fatality

# remove the spkkace in the column name for better syntax and readability

data = data.rename(columns = {'Fatal (Y/N)':'Fatality'})

# sort the unique values in column Fatality into three categories: No, Yes and Unknown

data['Fatality'] =  data['Fatality'].replace(['N', ' N', 'N '],'No')
data['Fatality'] =  data['Fatality'].replace(['Y'],'Yes')
data['Fatality'] =  data['Fatality'].replace(['UNKNOWN', 'M', '2017'],'Unknown')
data['Fatality'] = data['Fatality'].fillna('Unknown')

Mydata = data.groupby(['Fatality', 'Gender'], as_index=False).size()
Mydata = Mydata.sort_values(by=['size'], ascending=False)
Mydata = Mydata[0:7]
Mydata.drop([5],inplace=True)

Mydata.drop([4],inplace=True)
Mydata.drop([6],inplace=True)

import plotly.express as px
mlabels=['Male Non Fatal', 'Male Fatal','Female Non Fatal','Female Fatal']
fatality_fig = px.pie(Mydata, names=mlabels,values='size',hole = 0.8)
fatality_fig.update_traces(textposition='outside', textinfo='percent+label')
fatality_fig.update_layout(
    annotations=[dict(text="comparison of accidents", x=0.5, y=0.5, font_size=20, showarrow=False)])
fatality_fig.update_layout(showlegend=False)
fatality_fig.update_layout(height=500, width=600)


# Location
# Top 10 countries by no. of attacks

top_10_countries = data[data.Type == 'AllType'].groupby('Country')['Country'].count().sort_values(ascending=False)[:10]

top_10_countries = px.bar(top_10_countries, x=top_10_countries.values, y=top_10_countries.index, orientation='h', labels={'index':'','x':'Shark attacks'}, color = 'Country')
top_10_countries.update_layout(height=600, width=900)
top_10_countries.show()

# Attacks by country

attacks_by_country = data['Country'].value_counts().reset_index().rename(columns={'Country':'Count','index':'Country'})
attacks_by_country.head()

# World map of attacks by country
world_map = px.choropleth(attacks_by_country,
                    locations = 'Count',
                    color = 'Count',
                    color_continuous_scale='Plasma',
                    locationmode = 'country names',
                    scope = 'world',
                    title = 'Shark attacks around the World',
                    labels = {'Count':'Shark attacks'}
                    )

world_map.update_geos(fitbounds="locations", visible=False)
world_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

world_map.show()

st.set_page_config(page_title='Shark Attacks - Dashboard 🦈',
                    page_icon='🦈',
                    layout='wide')

st.title('Shark Attacks 🦈')

tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Gender and fatality", "Attacks around the world", "Activities and year"])

with tab1:
    st.header('Introduction to the dashboard')
    st.text('Every year, shark attacks occur around the world. Despite their rarity, many people fear attacks when going into water.')
    st.text('By understanding who, where and during which activities shark attacks occur, it is possible to lessen the likelihood')
    st.text(' of these incidents happending and thereby the fear among individuals.')
    st.text('')
    st.text('Browse the tabs to get insightful information about shark attacks.')
    st.text('')
    st.text('')
    st.text('▶️ But first, press PLAY on the audio and video! ▶️')
    st.text('')
    st.text('')
    st.audio('https://www.televisiontunes.com/uploads/audio/Jaws.mp3')
    st.video('https://www.youtube.com/watch?v=4HGNqFdaD34&t=5s')

with st.sidebar:
    
    "Made by Group 3"
    "Nadia"
    "Fredrik"
    "Jakob"
    "Alpha"
    "Sadiksha"
    "Jannatul"

with tab2:
   st.header("Do sharks gender discriminate when deciding their dinner?")
   col1, col2 = st.columns(2)
   with col1:
        st.subheader("Attacks by Gender")
        st.plotly_chart(gender_fig, use_container_width=True)
           
        with st.expander("Gender"):
            st.write("""
                Males seems to be the optimal choice for dinner compared to females.
            """)
            
   with col2:
        st.subheader("Fatality by Gender")
        st.plotly_chart(fatality_fig, use_container_width=True)
     
        with st.expander("Fatality"):
            st.write("""
                It seems the sharks need to attend shark-university to become better predators. Almost 75% of their attacks are non-fatal
            """)



with tab3:
    st.header("Drag, zoom and hover over the map to see where the sharks find their dinner")
    st.plotly_chart(world_map, use_container_width=True)
    st.plotly_chart(top_10_countries, use_container_width=True)



with tab4:
    st.header("Take a look at which activities to avoid if you do not want to get eaten by a shark")
    st.plotly_chart(activity_fig, use_container_width=True)
    st.plotly_chart(year_fig, use_container_width=True)
