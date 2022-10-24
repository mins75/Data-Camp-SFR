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

import datetime

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
#st.subheader("Brade Adam-Myn Sonya") 

#st.sidebar.title("Navigation Bar")
#st.sidebar.button("Click")
#st.sidebar.radio("Choose you gender",["Male", "Female"])

######

st.set_page_config(
    page_title="SFRate Dashbaord",
    layout="wide",
    page_icon="images/Logo_SFR_2014.png",
)

@st.cache(suppress_st_warning=True) #let our app to be performant
def get_database(): 
    #df1 = pd.read_feather('DataSFRpart1.fth')
    #df2 = pd.read_feather('DataSFRpart2.fth')
    df1 = pd.read_csv('data1.csv').reset_index(drop=True)
    df2 = pd.read_csv('data2.csv').reset_index(drop=True)
    df3 = pd.read_csv('data3.csv').reset_index(drop=True)
    df4 = pd.read_csv('data4.csv').reset_index(drop=True)
    df5 = pd.read_csv('data5.csv').reset_index(drop=True)
    df = pd.concat([df1,df2,df3,df4,df5]).reset_index(drop=True)
    #df = df.drop(columns='Unnamed: 0')
    #df = pd.concat([df1,df2]).reset_index(drop=True)
    #df = pd.read_csv('DataSFR.csv')
    df.Tweet_date = pd.to_datetime(df.Tweet_date).dt.date
    df.month_year = pd.to_datetime(df.month_year).dt.date
    return df

with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as response:
        geo = json.load(response)

def map_dpt_value(df,zoom=4,width=500,height=500,lat=46.5,lon=3):

        df = df[['DEP','sentiment_score']]

        df = df.groupby('DEP').mean().reset_index()

        fig = go.Figure(
            go.Choroplethmapbox(
                geojson=geo,
                locations=df.DEP,
                featureidkey="properties.code",
                z=df.sentiment_score,
                colorscale="sunsetdark",
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
        return fig
    
def lineplot(df,xname,yname,title):
    #df_chart = df[[col1,col2]].groupby(col1).mean().reset_index(drop=True)
    df_chart = df[['month_year','sentiment_score']].groupby('month_year').mean().reset_index()
    #df_chart = df[['year','month','se']].groupby([(df.year), (df.month)]).mean().reset_index(drop=True)
    df_chart['sentiment_score'] = df_chart['sentiment_score'].round(3)
    fig = px.line(df_chart, x=df_chart.month_year, y=df_chart.sentiment_score, 
                    labels={
                     "Month and year": xname,
                     "Sentiment score": yname,
                    },
                    title = title,
                    text=df_chart['sentiment_score'], orientation='h')

    return fig

def piechart(df,xname,yname,title):
    df_chart =  pd.DataFrame(df.sentiment_score.value_counts()).reset_index().rename(columns={'index':'sentiment_score','sentiment_score':'count'}).sort_values('sentiment_score')
    fig = px.pie(df_chart, values='count', names='sentiment_score', title='Piechart of the sentiment score count')
    return fig

###########################
#
#   INITIALIZE DATAFRAME
#
########################

df = get_database()

#########################
#
#       SIDEBAR
#
########################

app_mode = st.sidebar.selectbox('Select Page',['Home','Summary','Graphs','Trends']) # we have until now 2 pages, home for visualizing

agree = st.sidebar.checkbox('Add a keyword ?')

if agree:
    service = st.sidebar.text_input('Choose a keyword :')

    #service = str(' '+service+' ')
    st.sidebar.write(service)    

    df_filtered = df[df.Tweet.str.contains(service)].reset_index(drop=True)
else : 
    df_filtered = df.copy()
#st.sidebar.dataframe(df_filtered.head())

date = st.sidebar.date_input("Choose the time period :", value=[datetime.date(2020, 1, 1),datetime.date(2021, 12, 31)],
                            min_value=datetime.date(2007, 7, 4), max_value=datetime.date(2022,10,18))

#st.sidebar.write(date[0])
#st.sidebar.write(date[1])

date1 = date[0]
date2 = date[1]

df_filtered_date = df_filtered[df_filtered.Tweet_date.between(date1,date2)].reset_index(drop=True)
#st.sidebar.dataframe(df_filtered_date.head())

agree2 = st.sidebar.checkbox('Add a Location ?')

if agree2:
    dep = st.sidebar.selectbox("Choose the dpt : ",('75', '93', '33', '69', '57', '44', '59', '49', '92', '42', '31',
       '09', '35', '78', '02', '67', '48', '34', '06', '21', '68', '19',
       '76', '16', '38', '13', '56', '11', '28', '25', '66', '18', '37',
       '29', '17', '51', '89', '36', '74', '45', '07', '64', '60', '14',
       '10', '43', '54', '24', '01', '04', '77', '80', '41', '91', '40',
       '86', '63', '62', '53', '84', '03', '87', '94', '71', '30', '08',
       '2A', '22', '27', '88', '47', '61', '70', '95', '50', '83', '55',
       '73', '46', '81', '2B', '79', '974', '82', '65', '32', '58', '12',
       '85', '72', '39', '52', '971', '05', '90', '15', '26', '972', '23',
       '976', '973'))
    st.sidebar.write('You chose : ',dep)
    df_filtered_date = df_filtered_date[df_filtered_date.DEP==dep].reset_index(drop=True)
else :
    df_filtered_date = df_filtered[df_filtered.Tweet_date.between(date1,date2)].reset_index(drop=True)

###########################
#
#       CODE
#
############################



if app_mode =='Home': 
    st.title('Welcome to the SFRate dashboard ! ')

if app_mode =='Summary':
    st.title('Summary : Most liked tweet during this time period ')

    most_liked = df_filtered_date[df_filtered_date.LikeCount == max(df_filtered_date.LikeCount)]
    st.write('Tweet from : '+str(most_liked.User.unique()[0]))
    st.write('Tweet : '+str(most_liked.Tweet.unique()[0]))
    st.write('Score : '+str(most_liked.sentiment_score.unique()[0]))

    col1, col2, col3 = st.columns(3)
    #st.metric()
    with col1:
        st.metric('Number of retweets : ',str(most_liked.RetweetCount.unique()[0]))
    with col2:
        st.metric('Number of likes : ',str(most_liked.LikeCount.unique()[0]))
    with col3:
        delta = round(most_liked.sentiment_score.unique()[0] - df_filtered_date.sentiment_score.mean(),2)
        st.metric('Sentiment score : ',str(most_liked.sentiment_score.unique()[0]),delta)
        
	
    
if app_mode == 'Graphs' :
    st.title('Graphs')
    col1,col2 = st.columns(2)

    #LINECHART

    with col1:
        fig1 = lineplot(df_filtered_date,'Month','Sentiment score', 'Sentiment score depending on the month and year')
        st.plotly_chart(fig1,use_container_width=True)
        fig3 = px.histogram(df_filtered_date, x="month_year",color='sentiment_score',title = 'Histogram of the tweets depending on the time')
        st.plotly_chart(fig3,use_container_width=True)

    #MAP
    with col2:
        fig2 = map_dpt_value(df_filtered_date)
        st.plotly_chart(fig2,use_container_width=True)
        fig4 = px.pie(df_filtered_date, values='sentiment_score', names='sentiment_score', color_discrete_sequence=px.colors.sequential.RdBu,
        title='Piechart of the sentiment score count')
        st.plotly_chart(fig4,use_container_width=True)


if app_mode == 'Trends':
    st.title('Heatmap of the score')

    agree3 = st.checkbox('Add the departement filter to the heatmap ?')

    if agree3:
        df_filtered_dpt = df_filtered[df_filtered.DEP==dep].reset_index(drop=True)
    else :
        df_filtered_dpt = df_filtered.copy()



    df_cross = df_filtered_dpt.groupby(['year','month'])['sentiment_score'].mean().unstack()
    fig5 = go.Figure(data=go.Heatmap(
                   z=df_cross.to_numpy(),
                   x=["Jan",'Feb','Mar','Apr','May','June','July','August','Sept','Oct','Nov','Dec'],
                   y=['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'],
                   hoverongaps = False))
    st.plotly_chart(fig5,use_container_width=True)
    #heatmap
    




    






# %%
