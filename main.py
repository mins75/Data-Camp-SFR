#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.figure_factory as ff
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

from urllib.request import urlopen
import json

# In[3]:


#def main () :
#headerSection = st.container()
#mainSection = st.container()
#navig = st.sideBar
    
#with headerSection: 
    #st.title("SFRate")
 #   st.markdown("Project DataCamp")
#this next part will probably change it's just a test  
#st.title ("SFRate")
#st.header("Data Engineering")
#st.markdown("Data Camp 2022 2023 DE 2")
#st.subheader("Brade Adamyn Sonya") 

#st.sidebar.title("Navigation Bar")
#st.sidebar.button("Click")
#st.sidebar.radio("Choose you gender",["Male", "Female"])

######
@st.cache(suppress_st_warning=True) #let our app to be performant
def get_fvalue(val): 
    feature_dict = {"No":1,"Yes":2}
    for key, valuer in feature_dict.items():
        if val == key: 
            return val
        
def get_value(val, my_dict): 
    for key,value in my_dict.items():
        if val == key :
            return value

with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as response:
        geo = json.load(response)

def map_dpt_value(df,zoom=4.5,width=800,height=800,lat=46.5,lon=3):
        fig = go.Figure(
            go.Choroplethmapbox(
                geojson=geo,
                locations=df.DEP,
                featureidkey="properties.code",
                z=df.sentiment_score,
                colorscale="sunsetdark",
                # zmin=0,
                # zmax=500000,
                marker_opacity=0.5,
                marker_line_width=0,
            )
        )
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=zoom,
            mapbox_center={"lat":lat,"lon":lon},
            width=width,
            height=height,
        )
        return st.plotly_chart(fig,use_container_width=True)
    
app_mode = st.sidebar.selectbox('Select Page',['Home','Pred']) # we have until now 2 pages, home for visualizing

if app_mode =='Home': 
    st.title('About SFR : ')
    #st.image('logosfr.jpg')
    #df = pd.read_feather('All_data.fth')
    #df = pd.read_csv('data.csv')
    df2 = pd.read_feather('data.fth')
    df2 = df2[df2.User.str.contains('SFR')==False]

    dfbis = df2.copy()
    dfbis = dfbis[['DEP','sentiment_score']]

    dfbis = dfbis.groupby('DEP').median().reset_index()
    #df['Tweet_date'] = pd.to_datetime(df['Tweet_date'])
    #df['month'] = df.Tweet_date.dt.month
    st.write(df2.head())
    st.markdown('Period VS Sentiment Score Norm')
    #df_chart = pd.DataFrame(
    #    np.random.randn(20, 3),
    #    columns =['month','sentiment_score_norm'])
    df_chart = df2[['month','sentiment_score_norm']].groupby('month').median()
    
    fig = px.box(x=df2['month'], y=df2["sentiment_score_norm"])

    st.line_chart(df_chart) #[['year','month','day','sentiment_score_norm']].head(20))

    st.plotly_chart(fig)
    
    map_dpt_value(dfbis)

    service = st.text_input('choose a service')
    service = str(' '+service+' ')
    st.write(service)

    df = df2[df2.Tweet.str.contains(service)]
    st.dataframe(df.head())



