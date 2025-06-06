import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from math import ceil
from datetime import date
from streamlit_dynamic_filters import DynamicFilters
import urllib.request
from PIL import Image
import time
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n, sample_frac, head, arrange, mutate, group_by, summarize, DelayFunction)
from itables.streamlit import interactive_table
from itables import to_html_datatable
from streamlit.components.v1 import html
from plotly.subplots import make_subplots
st.set_page_config(layout='wide', page_title="Standings")
dataset2223=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2223.csv")
dataset2324=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2324.csv")
dataset2425=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")
dataset=pd.concat([dataset2324,dataset2425,dataset2223])
f1,f2,f3,f4,f5=st.columns(5)
with f1:
    selected_season = st.selectbox("Season:", ['All', '2022-2023', '2023-2024', '2024-2025'], index=3)
with f2:
    selected_phase = st.selectbox("Phase:", ['Regular Season', 'Play offs', "Play In", 'Play out', 'All'], index=4)
with f3:
    selected_round = st.selectbox("Round:", ['First Round', 'Second Round', 'All'], index=2)
with f4:
    selected_ha = st.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
with f5:
    selected_wl = st.selectbox("Result:",['Win','Draw', 'Lose','All'],index=3)

teamsscored=dataset.groupby(['Team','Against','idseason'])[['Goals','Own goals']].sum().reset_index().rename(columns={'Goals':'Goals Team','Own goals':'Own goals Against'})
againstscored=teamsscored.rename(columns={'Goals Team':'Goals Against','Own goals Against':'Own goals Team'})
againstscored.drop('Against',axis=1,inplace=True)
againstscored=againstscored.rename(columns={'Team':'Against'})
goals=pd.merge(teamsscored,againstscored,how='left')

goals['Goals Scored']=goals['Goals Team']+goals['Own goals Team']
goals['Goals Conceed']=goals['Goals Against']+goals['Own goals Against']

infodataset=dataset.groupby( ['Team', 'Against', 'idseason', 'Home_Away', 'Season', 'Round', 'Result','Phase']).count().reset_index()[['Team', 'Against', 'idseason', 'Home_Away', 'Season', 'Round', 'Result','Phase']]
goals=pd.merge(infodataset,goals)



if "All" in selected_ha:
    selected_ha = ['Away', 'Home']
    dataset_filter=dataset.loc[dataset['Home_Away'].isin(selected_ha)]
    goals_filter = goals.loc[goals['Home_Away'].isin(selected_ha)]
    select_ha=''
else:
    dataset_filter=dataset.loc[dataset['Home_Away']==selected_ha]
    goals_filter = goals.loc[goals['Home_Away'] == selected_ha]
    select_ha = selected_ha

if "All" in selected_season:
    selected_season = [ '2022-2023','2023-2024','2024-2025']
    dataset_filter=dataset_filter.loc[dataset_filter['Season'].isin(selected_season)]
    goals_filter = goals_filter.loc[goals_filter['Season'].isin(selected_season)]
    select_season = ''
else:
    dataset_filter=dataset_filter.loc[dataset_filter['Season']==selected_season]
    goals_filter = goals_filter.loc[goals_filter['Season'] == selected_season]
    select_season = selected_season

if "All" in selected_wl:
    selected_wl = ['Win','Draw', 'Lose']
    dataset_filter = dataset_filter.loc[dataset_filter['Result'].isin(selected_wl)]
    goals_filter = goals_filter.loc[goals_filter['Result'].isin(selected_wl)]
    select_wl = ''
else:
    dataset_filter= dataset_filter.loc[dataset_filter['Result'] == selected_wl]
    goals_filter = goals_filter.loc[goals_filter['Result'] == selected_wl]
    select_wl = selected_wl

if "All" in selected_phase:
    selected_phase = ['Regular Season', 'Play offs', "Play In",'Play out']
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'].isin(selected_phase)]
    goals_filter = goals_filter.loc[goals_filter['Phase'].isin(selected_phase)]
    select_phase = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'] == selected_phase]
    goals_filter = goals_filter.loc[goals_filter['Phase']==selected_phase]
    select_phase = selected_phase

if "All" in selected_round:
    selected_round = ['First Round', 'Second Round' ]
    dataset_filter = dataset_filter.loc[dataset_filter['Round'].isin(selected_round)]
    goals_filter = goals_filter.loc[goals_filter['Round'].isin(selected_round)]
    select_round = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Round'] == selected_round]
    goals_filter = goals_filter.loc[goals_filter['Round'] == selected_round]
    select_round = selected_round


games=dataset_filter[['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Games'})
wins=dataset_filter.loc[dataset_filter.Result=='Win'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Wins'})
loses=dataset_filter.loc[dataset_filter.Result=='Lose'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Loses'})
draws=dataset_filter.loc[dataset_filter.Result=='Draw'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Draws'})

Team_Standings=pd.merge(games,wins,how='left',on='Team')
Team_Standings=pd.merge(Team_Standings,draws,how='left',on='Team')
Team_Standings=pd.merge(Team_Standings,loses,how='left',on='Team')
Team_Standings['Wins']=Team_Standings['Wins'].fillna(0)
Team_Standings['Loses']=Team_Standings['Loses'].fillna(0)
Team_Standings['Draws']=Team_Standings['Draws'].fillna(0)
Team_Standings['Points']=Team_Standings['Wins']*3+Team_Standings['Draws']*1

total_goals=goals_filter.groupby('Team')[['Goals Scored','Goals Conceed']].sum().reset_index()




Team_Standings=pd.merge(Team_Standings,total_goals,how='left',on='Team').sort_values('Points',ascending=False).reset_index()
Team_Standings.drop('index',axis=1,inplace=True)
Team_Standings=Team_Standings.reset_index()
Team_Standings['Rank']=Team_Standings['index']+1
Team_Standings.drop('index',axis=1,inplace=True)
Team_Standings=Team_Standings[['Rank','Team','Points','Games','Wins','Draws','Loses','Goals Scored','Goals Conceed']]

interactive_table(Team_Standings.set_index('Rank'),
                      paging=False,height=960,width=20000,showIndex=True,classes="display order-column nowrap table_with_monospace_font",searching=False,fixedColumns=True,select=True,info=False,scrollCollapse=True,
        scrollX=True,scrollY=1000,fixedHeader=True,scroller=True,columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('2023-2024: Olympiacos-Panathinaikos on Regular Season had postponed due to riots and could not record data')
