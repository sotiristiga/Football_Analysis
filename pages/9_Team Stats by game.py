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

dataset=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")

selected_Team1 = st.sidebar.selectbox("Choose First Team:", dataset['Team'].reset_index().sort_values('Team')['Team'].unique())
selected_ha1 = st.sidebar.selectbox("Home or Away games (First Team):",['Away', 'Home', 'All'],index=2)
selected_season1 = st.sidebar.selectbox("Season (First Team):",['All','2024-2025'],index=0)
selected_phase1 = st.sidebar.selectbox("Phase (First Team):",['Regular Season', 'Play offs', 'Play out','All'],index=3)
selected_wl1 = st.sidebar.selectbox("Result (First Team):",['Win','Draw', 'Lose','All'],index=3)
selected_round1 = st.sidebar.selectbox("Round (First Team):",['First Round', 'Second Round', 'All'],index=2)


if "All" in selected_ha1:
    selected_ha1 = ['Away', 'Home',]
    dataset_filter1=dataset.loc[dataset['Home_Away'].isin(selected_ha1)]
    select_ha1=''
else:
    dataset_filter1=dataset.loc[dataset['Home_Away']==selected_ha1]
    select_ha1 = selected_ha1

if "All" in selected_season1:
    selected_season1 = ['2016-2017', '2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022', '2022-2023','2023-2024','2024-2025']
    dataset_filter1=dataset_filter1.loc[dataset_filter1['Season'].isin(selected_season1)]
    select_season1 = ''
else:
    dataset_filter1=dataset_filter1.loc[dataset_filter1['Season']==selected_season1]
    select_season1 = selected_season1

if "All" in selected_wl1:
    selected_wl1 = ['Win','Draw', 'Lose']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Result'].isin(selected_wl1)]
    select_wl1 = ''
else:
    dataset_filter1= dataset_filter1.loc[dataset_filter1['Result'] == selected_wl1]
    select_wl1 = selected_wl1

if "All" in selected_phase1:
    selected_phase1 = ['Regular Season', 'Play offs', 'Play out']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Phase'].isin(selected_phase1)]
    select_phase1 = ''
else:
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Phase'] == selected_phase1]
    select_phase1 = selected_phase1

if "All" in selected_round1:
    selected_round1 = ['First Round', 'Second Round', ]
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Round'].isin(selected_round1)]
    select_round1 = ''
else:
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Round'] == selected_round1]
    select_round1 = selected_round1

try:
    allstats,selectstat=st.tabs(['All Stats','Select Stats'])
    with allstats:
        computeTeamstats_on_games=dataset_filter1.groupby(["idseason",'Team','Against','Home_Away','Result','Season','Phase','Round','Fixture'])[[
           'Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
           'Shots off target', 'Shots blocked', 'Dribble attempts',
           'Dribble attempts succ', 'Penalty won', 'Big chances missed',
           'Penalty miss', 'Hit woodwork', 'Defensive actions', 'Clearances',
           'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
           'Penalty committed', 'Own goals', 'Last man tackle',
           'Error led to shot', 'Clearance off line', 'Error led to goal',
           'Touches', 'Accurate passes', 'Total passes',
           'Key passes', 'Total Crosses', 'Accurate Crosses', 'Total Long balls',
           'Accurate Long balls', 'Big chances created', 'Duels', 'Duels won',
           'Ground duels', 'Ground duels won', 'Aerial duels', 'Aerial duels won',
           'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
           'Punches', 'Runs out', 'Runs out succ', 'High claims',
           'Saves from inside box', 'Penalties saved']].sum().reset_index()
        computeTeamstats_on_games["Dribble(%)"]=(100*computeTeamstats_on_games["Dribble attempts succ"]/computeTeamstats_on_games["Dribble attempts"]).round(1)
        computeTeamstats_on_games["Dribble(%)"]=computeTeamstats_on_games["Dribble(%)"].fillna(0)
        computeTeamstats_on_games["Passes(%)"] = (100 * computeTeamstats_on_games["Accurate passes"] / computeTeamstats_on_games["Total passes"]).round(1)
        computeTeamstats_on_games["Passes(%)"] = computeTeamstats_on_games["Passes(%)"].fillna(0)
        computeTeamstats_on_games["Crosses(%)"] = (100 * computeTeamstats_on_games["Accurate Crosses"] / computeTeamstats_on_games["Total Crosses"]).round(1)
        computeTeamstats_on_games["Crosses(%)"] = computeTeamstats_on_games["Crosses(%)"].fillna(0)
        computeTeamstats_on_games["Long balls(%)"] = (100 * computeTeamstats_on_games["Accurate Long balls"] / computeTeamstats_on_games["Total Long balls"]).round(1)
        computeTeamstats_on_games["Long balls(%)"] = computeTeamstats_on_games["Long balls(%)"].fillna(0)
        computeTeamstats_on_games["Duels(%)"] = (100 * computeTeamstats_on_games["Duels won"] / computeTeamstats_on_games["Duels"]).round(1)
        computeTeamstats_on_games["Duels(%)"] = computeTeamstats_on_games["Duels(%)"].fillna(0)
        computeTeamstats_on_games["Aerial duels(%)"] = (100 * computeTeamstats_on_games["Aerial duels won"] / computeTeamstats_on_games["Aerial duels"]).round(1)
        computeTeamstats_on_games["Aerial duels(%)"] = computeTeamstats_on_games["Aerial duels(%)"].fillna(0)
        computeTeamstats_on_games["Ground duels(%)"] = (100 * computeTeamstats_on_games["Ground duels won"] / computeTeamstats_on_games["Ground duels"]).round(1)
        computeTeamstats_on_games["Ground duels(%)"] = computeTeamstats_on_games["Ground duels(%)"].fillna(0)
        computeTeamstats_on_games["Runs out(%)"] = (100 * computeTeamstats_on_games["Runs out succ"] / computeTeamstats_on_games["Runs out"]).round(1)
        computeTeamstats_on_games["Runs out(%)"] = computeTeamstats_on_games["Runs out(%)"].fillna(0)



        computeAgainststats_on_games=dataset_filter1.groupby(['idseason','Against'])[[
               'Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
               'Shots off target', 'Shots blocked', 'Dribble attempts',
               'Dribble attempts succ', 'Penalty won', 'Big chances missed',
               'Penalty miss', 'Hit woodwork', 'Defensive actions', 'Clearances',
               'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
               'Penalty committed', 'Own goals', 'Last man tackle',
               'Error led to shot', 'Clearance off line', 'Error led to goal',
               'Touches', 'Accurate passes', 'Total passes',
               'Key passes', 'Total Crosses', 'Accurate Crosses', 'Total Long balls',
               'Accurate Long balls', 'Big chances created', 'Duels', 'Duels won',
               'Ground duels', 'Ground duels won', 'Aerial duels', 'Aerial duels won',
               'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
               'Punches', 'Runs out', 'Runs out succ', 'High claims',
               'Saves from inside box', 'Penalties saved']].sum().reset_index()
        computeAgainststats_on_games["Dribble(%)"]=(100*computeAgainststats_on_games["Dribble attempts succ"]/computeAgainststats_on_games["Dribble attempts"]).round(1)
        computeAgainststats_on_games["Dribble(%)"]=computeAgainststats_on_games["Dribble(%)"].fillna(0)
        computeAgainststats_on_games["Passes(%)"] = (100 * computeAgainststats_on_games["Accurate passes"] / computeAgainststats_on_games["Total passes"]).round(1)
        computeAgainststats_on_games["Passes(%)"] = computeAgainststats_on_games["Passes(%)"].fillna(0)
        computeAgainststats_on_games["Crosses(%)"] = (100 * computeAgainststats_on_games["Accurate Crosses"] / computeAgainststats_on_games["Total Crosses"]).round(1)
        computeAgainststats_on_games["Crosses(%)"] = computeAgainststats_on_games["Crosses(%)"].fillna(0)
        computeAgainststats_on_games["Long balls(%)"] = (100 * computeAgainststats_on_games["Accurate Long balls"] / computeAgainststats_on_games["Total Long balls"]).round(1)
        computeAgainststats_on_games["Long balls(%)"] = computeAgainststats_on_games["Long balls(%)"].fillna(0)
        computeAgainststats_on_games["Duels(%)"] = (100 * computeAgainststats_on_games["Duels won"] / computeAgainststats_on_games["Duels"]).round(1)
        computeAgainststats_on_games["Duels(%)"] = computeAgainststats_on_games["Duels(%)"].fillna(0)
        computeAgainststats_on_games["Aerial duels(%)"] = (100 * computeAgainststats_on_games["Aerial duels won"] / computeAgainststats_on_games["Aerial duels"]).round(1)
        computeAgainststats_on_games["Aerial duels(%)"] = computeAgainststats_on_games["Aerial duels(%)"].fillna(0)
        computeAgainststats_on_games["Ground duels(%)"] = (100 * computeAgainststats_on_games["Ground duels won"] / computeAgainststats_on_games["Ground duels"]).round(1)
        computeAgainststats_on_games["Ground duels(%)"] = computeAgainststats_on_games["Ground duels(%)"].fillna(0)
        computeAgainststats_on_games["Runs out(%)"] = (100 * computeAgainststats_on_games["Runs out succ"] / computeAgainststats_on_games["Runs out"]).round(1)
        computeAgainststats_on_games["Runs out(%)"] = computeAgainststats_on_games["Runs out(%)"].fillna(0)



        computeAgainststats_on_games=computeAgainststats_on_games.add_prefix('opp ').rename(columns={'opp Against':'Team','opp idseason':'idseason'})

        computeteamstats_on_games_total=pd.merge(computeTeamstats_on_games,computeAgainststats_on_games,on=['Team','idseason'])
        computeteamstats_on_games_total_sel=computeteamstats_on_games_total.loc[computeteamstats_on_games_total.Team==selected_Team1]
        finaldataset=computeteamstats_on_games_total_sel[['Against','Season','Phase','Round','Fixture','Home_Away','Result',"Goals", "opp Goals", 'Assists', 'opp Assists', 'Yellow card', 'opp Yellow card', 'Red card',
                 'opp Red card','Shots on target', 'opp Shots on target','Shots off target','opp Shots off target','Shots blocked','opp Shots blocked', 'Dribble attempts succ','opp Dribble attempts succ',
                 'Dribble attempts','opp Dribble attempts', "Dribble(%)","opp Dribble(%)",'Penalty won', 'Big chances missed','opp Big chances missed','Penalty miss','opp Penalty miss',
                 'Hit woodwork','opp Hit woodwork', 'Offsides', 'opp Offsides','Defensive actions', 'opp Defensive actions','Clearances','opp Clearances',
          'Interceptions', 'opp Interceptions','Total tackles', 'opp Total tackles','Dribbled past',
           'Penalty committed', 'Own goals', 'opp Own goals','Last man tackle','opp Last man tackle',
           'Error led to shot', 'opp Error led to shot', 'Clearance off line', 'opp Clearance off line','Error led to goal', 'opp Error led to goal','Duels won',"Duels(%)",
            'opp Duels won',"opp Duels(%)",'Ground duels', 'Ground duels won',"Ground duels(%)", 'opp Ground duels won',"opp Ground duels(%)",
            'Aerial duels', 'Aerial duels won',"Aerial duels(%)", 'opp Aerial duels won',"opp Aerial duels(%)",'Possession lost',  'opp Possession lost',
            'Fouls', 'opp Fouls','Touches','opp Touches', 'Accurate passes', 'Total passes',"Passes(%)",'opp Accurate passes','opp Total passes', "opp Passes(%)",'Key passes','opp Key passes',
             'Total Crosses', 'Accurate Crosses',"Crosses(%)",'opp Total Crosses','opp Accurate Crosses',"opp Crosses(%)",'Total Long balls','Accurate Long balls',"Long balls(%)",
             'opp Total Long balls','opp Accurate Long balls',"opp Long balls(%)",'Big chances created','opp Big chances created','Saves','opp Saves',
           'Punches','opp Punches', 'Runs out', 'Runs out succ', "Runs out(%)",'opp Runs out','opp Runs out succ',"opp Runs out(%)",
           'High claims', 'opp High claims','Saves from inside box', 'opp Saves from inside box', 'Penalties saved', 'opp Penalties saved']].rename(columns={ 'Accurate passes': 'Accurate Passes','Total passes':'Total Passes','Key passes':'Key Passes', 'opp Accurate passes':'opp Accurate Passes',
            'opp Total passes':'opp Total Passes','opp Key passes':'opp Key Passes','Penalties saved':'Penalty saved','opp Penalties saved':'opp Penalty saved','Clearance off line':'Clearances off line', 'opp Clearance off line':'opp Clearances off line'})

        interactive_table(finaldataset.set_index('Against'),
            paging=False, height=900, width=2000, showIndex=True,
                    classes="display order-column nowrap table_with_monospace_font", searching=True,
                    fixedColumns=True, select=True, info=False, scrollCollapse=True,
                    scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                    columnDefs=[{"className": "dt-center", "targets": "_all"}])
        with selectstat:
            statselectors = st.selectbox("Select Stat:", ['Goals', 'Assists', 'Yellow card', 'Red card','Shots',  'Dribble', 'Penalty', 'Big chances','Hit woodwork', 'Offsides',
                                                          'Defensive actions', 'Clearances', 'Interceptions', 'Total tackles',
                                                          'Own goals', 'Last man tackle','Error led to shot',  'Error led to goal','Duels','Ground duels',  'Aerial duels',
                                                            'Possession lost', 'Foul','Touches','Passes','Crosses',  'Long balls','Saves','Punches', 'Runs out','High claims'])
            regex1 = "Against|Season|Phase|Round|Fixture|Home_Away|Result|"+statselectors

            interactive_table(finaldataset.filter(regex=regex1).set_index('Against'),
                              paging=False, height=900, width=2000, showIndex=True,
                              classes="display order-column nowrap table_with_monospace_font", searching=True,
                              fixedColumns=True, select=True, info=False, scrollCollapse=True,
                              scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                              columnDefs=[{"className": "dt-center", "targets": "_all"}])
except:
    st.error('No data available for these parameters')

