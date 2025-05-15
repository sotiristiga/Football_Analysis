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



st.set_page_config(layout='wide', page_title="League Leaders on Team Stats")

dataset2223=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2223.csv")
dataset2324=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2324.csv")
dataset2425=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")
dataset=pd.concat([dataset2324,dataset2425,dataset2223])
st.sidebar.markdown('''
  * ## [Filters](#filters)
  * ## [Basic Stats](#basic-stats)
  * ## [Attack Stats](#attack-stats)
  * ## [Defence Stats](#defence-stats)
  * ## [Duels Stats](#duels-stats)
  * ## [Passing Stats](#passing-stats)
  * ## [Goalkeeping Stats](#goalkeeping-stats)   

''', unsafe_allow_html=True)
st.header("Filters")
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


if "All" in selected_ha:
    selected_ha = ['Away', 'Home',]
    dataset_filter=dataset.loc[dataset['Home_Away'].isin(selected_ha)]
    select_ha=''
else:
    dataset_filter=dataset.loc[dataset['Home_Away']==selected_ha]
    select_ha = selected_ha

if "All" in selected_season:
    selected_season = [ '2022-2023','2023-2024','2024-2025']
    dataset_filter=dataset_filter.loc[dataset_filter['Season'].isin(selected_season)]
    select_season = ''
else:
    dataset_filter=dataset_filter.loc[dataset_filter['Season']==selected_season]
    select_season = selected_season

if "All" in selected_wl:
    selected_wl = ['Win','Draw', 'Lose']
    dataset_filter = dataset_filter.loc[dataset_filter['Result'].isin(selected_wl)]
    select_wl = ''
else:
    dataset_filter= dataset_filter.loc[dataset_filter['Result'] == selected_wl]
    select_wl = selected_wl

if "All" in selected_phase:
    selected_phase = ['Regular Season', 'Play offs',  "Play In",'Play out']
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'].isin(selected_phase)]
    select_phase = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'] == selected_phase]
    select_phase = selected_phase

if "All" in selected_round:
    selected_round = ['First Round', 'Second Round', ]
    dataset_filter = dataset_filter.loc[dataset_filter['Round'].isin(selected_round)]
    select_round = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Round'] == selected_round]
    select_round = selected_round



computeTeamstats_on_games=dataset_filter.groupby(["idseason",'Team'])[[
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



computeAgainststats_on_games=dataset_filter.groupby(['idseason','Against'])[[
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



computeteamstats_on_games_mean=computeteamstats_on_games_total.groupby('Team')[['Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
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
       'Saves from inside box', 'Penalties saved',
        'opp Goals', 'opp Assists', 'opp Yellow card','opp Red card', 'opp Shots on target',
        'opp Shots off target', 'opp Shots blocked',
        'opp Dribble attempts',
        'opp Dribble attempts succ', 'opp Penalty won',
        'opp Big chances missed',
        'opp Penalty miss', 'opp Hit woodwork',
        'opp Defensive actions', 'opp Clearances',
        'opp Blocked shots', 'opp Interceptions',
        'opp Total tackles', 'opp Dribbled past',
        'opp Penalty committed', 'opp Own goals',
        'opp Last man tackle',
        'opp Error led to shot',
        'opp Clearance off line',
        'opp Error led to goal',
        'opp Touches', 'opp Accurate passes',
        'opp Total passes',
        'opp Key passes', 'opp Total Crosses',
        'opp Accurate Crosses', 'opp Total Long balls',
        'opp Accurate Long balls',
        'opp Big chances created', 'opp Duels',
        'opp Duels won',
        'opp Ground duels', 'opp Ground duels won',
        'opp Aerial duels', 'opp Aerial duels won',
        'opp Possession lost', 'opp Fouls',
        'opp Was fouled', 'opp Offsides', 'opp Saves',
        'opp Punches', 'opp Runs out', 'opp Runs out succ',
        'opp High claims',
        'opp Saves from inside box',
        'opp Penalties saved']].mean().reset_index().round(1)


computeteamstats_on_games_mean["Dribble(%)"]=(100*computeteamstats_on_games_mean["Dribble attempts succ"]/computeteamstats_on_games_mean["Dribble attempts"]).round(1)
computeteamstats_on_games_mean["Dribble(%)"]=computeteamstats_on_games_mean["Dribble(%)"].fillna(0)
computeteamstats_on_games_mean["Passes(%)"] = (100 * computeteamstats_on_games_mean["Accurate passes"] / computeteamstats_on_games_mean["Total passes"]).round(1)
computeteamstats_on_games_mean["Passes(%)"] = computeteamstats_on_games_mean["Passes(%)"].fillna(0)
computeteamstats_on_games_mean["Crosses(%)"] = (100 * computeteamstats_on_games_mean["Accurate Crosses"] / computeteamstats_on_games_mean["Total Crosses"]).round(1)
computeteamstats_on_games_mean["Crosses(%)"] = computeteamstats_on_games_mean["Crosses(%)"].fillna(0)
computeteamstats_on_games_mean["Long balls(%)"] = (100 * computeteamstats_on_games_mean["Accurate Long balls"] / computeteamstats_on_games_mean["Total Long balls"]).round(1)
computeteamstats_on_games_mean["Long balls(%)"] = computeteamstats_on_games_mean["Long balls(%)"].fillna(0)
computeteamstats_on_games_mean["Duels(%)"] = (100 * computeteamstats_on_games_mean["Duels won"] / computeteamstats_on_games_mean["Duels"]).round(1)
computeteamstats_on_games_mean["Duels(%)"] = computeteamstats_on_games_mean["Duels(%)"].fillna(0)
computeteamstats_on_games_mean["Aerial duels(%)"] = (100 * computeteamstats_on_games_mean["Aerial duels won"] / computeteamstats_on_games_mean["Aerial duels"]).round(1)
computeteamstats_on_games_mean["Aerial duels(%)"] = computeteamstats_on_games_mean["Aerial duels(%)"].fillna(0)
computeteamstats_on_games_mean["Ground duels(%)"] = (100 * computeteamstats_on_games_mean["Ground duels won"] / computeteamstats_on_games_mean["Ground duels"]).round(1)
computeteamstats_on_games_mean["Ground duels(%)"] = computeteamstats_on_games_mean["Ground duels(%)"].fillna(0)
computeteamstats_on_games_mean["Runs out(%)"] = (100 * computeteamstats_on_games_mean["Runs out succ"] / computeteamstats_on_games_mean["Runs out"]).round(1)
computeteamstats_on_games_mean["Runs out(%)"] = computeteamstats_on_games_mean["Runs out(%)"].fillna(0)


computeteamstats_on_games_mean["opp Dribble(%)"]=(100*computeteamstats_on_games_mean["opp Dribble attempts succ"]/computeteamstats_on_games_mean["opp Dribble attempts"]).round(1)
computeteamstats_on_games_mean["opp Dribble(%)"]=computeteamstats_on_games_mean["opp Dribble(%)"].fillna(0)
computeteamstats_on_games_mean["opp Passes(%)"] = (100 * computeteamstats_on_games_mean["opp Accurate passes"] / computeteamstats_on_games_mean["opp Total passes"]).round(1)
computeteamstats_on_games_mean["opp Passes(%)"] = computeteamstats_on_games_mean["opp Passes(%)"].fillna(0)
computeteamstats_on_games_mean["opp Crosses(%)"] = (100 * computeteamstats_on_games_mean["opp Accurate Crosses"] / computeteamstats_on_games_mean["opp Total Crosses"]).round(1)
computeteamstats_on_games_mean["opp Crosses(%)"] = computeteamstats_on_games_mean["opp Crosses(%)"].fillna(0)
computeteamstats_on_games_mean["opp Long balls(%)"] = (100 * computeteamstats_on_games_mean["opp Accurate Long balls"] / computeteamstats_on_games_mean["opp Total Long balls"]).round(1)
computeteamstats_on_games_mean["opp Long balls(%)"] = computeteamstats_on_games_mean["opp Long balls(%)"].fillna(0)
computeteamstats_on_games_mean["opp Duels(%)"] = (100 * computeteamstats_on_games_mean["opp Duels won"] / computeteamstats_on_games_mean["opp Duels"]).round(1)
computeteamstats_on_games_mean["opp Duels(%)"] = computeteamstats_on_games_mean["opp Duels(%)"].fillna(0)
computeteamstats_on_games_mean["opp Ground duels(%)"] = (100 * computeteamstats_on_games_mean["opp Ground duels won"] / computeteamstats_on_games_mean["opp Ground duels"]).round(1)
computeteamstats_on_games_mean["opp Ground duels(%)"] = computeteamstats_on_games_mean["opp Ground duels(%)"].fillna(0)
computeteamstats_on_games_mean["opp Aerial duels(%)"] = (100 * computeteamstats_on_games_mean["opp Aerial duels won"] / computeteamstats_on_games_mean["opp Aerial duels"]).round(1)
computeteamstats_on_games_mean["opp Aerial duels(%)"] = computeteamstats_on_games_mean["opp Aerial duels(%)"].fillna(0)
computeteamstats_on_games_mean["opp Runs out(%)"] = (100 * computeteamstats_on_games_mean["opp Runs out succ"] / computeteamstats_on_games_mean["opp Runs out"]).round(1)
computeteamstats_on_games_mean["opp Runs out(%)"] = computeteamstats_on_games_mean["opp Runs out(%)"].fillna(0)




st.header("Basic Stats")
basicselectors = st.selectbox("Select Stat:", ['Goals', 'Assists', 'Yellow card', 'Red card'])
total,pergame=st.tabs(['Total','Per Game'])
regex1="Team|"+basicselectors
with total:
    basic_total=computeteamstats_on_games_total.groupby('Team')[["Goals","opp Goals",'Assists','opp Assists','Yellow card','opp Yellow card','Red card','opp Red card']].sum().reset_index()
    interactive_table(basic_total.filter(regex=regex1).set_index('Team'),
    paging=False, height=900, width=100, showIndex=True,
    classes="display order-column nowrap table_with_monospace_font", searching=True,
    fixedColumns=True, select=True, info=False, scrollCollapse=True,
    scrollX=True, scrollY=600, fixedHeader=True, scroller=True, filter='left',
    columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    basic_mean=computeteamstats_on_games_mean[["Team","Goals","opp Goals",'Assists','opp Assists','Yellow card','opp Yellow card','Red card','opp Red card']]
    interactive_table(basic_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])


st.header("Attack Stats")

attackselectors=st.selectbox("Select Stat:",['Shots',  'Dribble', 'Penalty', 'Big chances missed','Hit woodwork', 'Offsides'])
total, pergame = st.tabs(['Total', 'Per Game'])
regex1 = "Team|" + attackselectors
with total:
    attack_total=computeteamstats_on_games_total.groupby('Team')[['Shots on target', 'opp Shots on target','Shots off target','opp Shots off target',
                                                                  'Shots blocked','opp Shots blocked', 'Dribble attempts succ','opp Dribble attempts succ',
         'Dribble attempts','opp Dribble attempts', 'Penalty won','opp Penalty won', 'Big chances missed',  'opp Big chances missed','Penalty miss','opp Penalty miss',
         'Hit woodwork','opp Hit woodwork', 'Offsides', 'opp Offsides']].sum().reset_index()
    attack_total["Dribble(%)"] = (100 * attack_total["Dribble attempts succ"] / attack_total["Dribble attempts"]).round(1)
    attack_total["Dribble(%)"] = attack_total["Dribble(%)"].fillna(0)
    attack_total["opp Dribble(%)"] = (100 * attack_total["opp Dribble attempts succ"] / attack_total["opp Dribble attempts"]).round(1)
    attack_total["opp Dribble(%)"] = attack_total["opp Dribble(%)"].fillna(0)
    interactive_table(attack_total.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    attack_mean=computeteamstats_on_games_mean[["Team",'Shots on target', 'opp Shots on target','Shots off target','opp Shots off target',
                                                                  'Shots blocked','opp Shots blocked', 'Dribble attempts succ','opp Dribble attempts succ',"Dribble(%)","opp Dribble(%)",
         'Dribble attempts','opp Dribble attempts', 'Penalty won','opp Penalty won', 'Big chances missed',  'opp Big chances missed','Penalty miss','opp Penalty miss',
         'Hit woodwork','opp Hit woodwork', 'Offsides', 'opp Offsides']]
    interactive_table(attack_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])


st.header("Defence Stats")

defenceselectors=st.selectbox("Select Stat:",['Defensive actions', 'Clearances',
   'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
   'Penalty committed', 'Own goals', 'Last man tackle',
   'Error led to shot', 'Clearance off line', 'Error led to goal'])
total, pergame = st.tabs(['Total', 'Per Game'])
regex1 = "Team|" + defenceselectors
with total:
    defence_total=computeteamstats_on_games_total.groupby('Team')[['Defensive actions', 'opp Defensive actions','Clearances','opp Clearances',
   'Blocked shots',  'opp Blocked shots','Interceptions', 'opp Interceptions','Total tackles', 'opp Total tackles','Dribbled past','opp Dribbled past',
   'Penalty committed', 'opp Penalty committed','Own goals', 'opp Own goals','Last man tackle','opp Last man tackle',
   'Error led to shot', 'opp Error led to shot', 'Clearance off line', 'opp Clearance off line','Error led to goal', 'opp Error led to goal']].sum().reset_index()
    interactive_table(defence_total.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    defence_mean=computeteamstats_on_games_mean[["Team",'Defensive actions', 'Clearances',
   'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
   'Penalty committed', 'Own goals', 'Last man tackle',
   'Error led to shot', 'Clearance off line', 'Error led to goal','opp Defensive actions', 'opp Clearances',
    'opp Blocked shots', 'opp Interceptions',
    'opp Total tackles', 'opp Dribbled past',
    'opp Penalty committed', 'opp Own goals',
    'opp Last man tackle',
    'opp Error led to shot',
    'opp Clearance off line',
    'opp Error led to goal']]
    interactive_table(defence_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.header("Duels Stats")

duelsselectors=st.selectbox("Select Stat:",['Duels',
   'Ground duels',  'Aerial duels',
   'Possession lost', 'Foul'])
total, pergame = st.tabs(['Total', 'Per Game'])
regex1 = "Team|" + duelsselectors
with total:
    duels_total=computeteamstats_on_games_total.groupby('Team')[['Duels', 'Duels won',
   'Ground duels', 'Ground duels won', 'Aerial duels', 'Aerial duels won',
   'Possession lost', 'Fouls', 'Was fouled','opp Duels',
    'opp Duels won',
    'opp Ground duels', 'opp Ground duels won',
    'opp Aerial duels', 'opp Aerial duels won',
    'opp Possession lost', 'opp Fouls']].sum().reset_index()
    duels_total["Duels(%)"] = (
                100 * duels_total["Duels won"] / duels_total["Duels"]).round(1)
    duels_total["Duels(%)"] = duels_total["Duels(%)"].fillna(0)
    duels_total["Aerial duels(%)"] = (
                100 * duels_total["Aerial duels won"] / duels_total[
            "Aerial duels"]).round(1)
    duels_total["Aerial duels(%)"] = duels_total["Aerial duels(%)"].fillna(0)
    duels_total["Ground duels(%)"] = (
                100 * duels_total["Ground duels won"] / duels_total[
            "Ground duels"]).round(1)
    duels_total["Ground duels(%)"] = duels_total["Ground duels(%)"].fillna(0)
    duels_total ["opp Duels(%)"] = (
            100 * duels_total ["opp Duels won"] / duels_total ["opp Duels"]).round(1)
    duels_total ["opp Duels(%)"] = duels_total ["opp Duels(%)"].fillna(0)
    duels_total ["opp Aerial duels(%)"] = (
            100 * duels_total ["opp Aerial duels won"] / duels_total[
        "opp Aerial duels"]).round(1)
    duels_total ["opp Aerial duels(%)"] = duels_total ["opp Aerial duels(%)"].fillna(0)
    duels_total ["opp Ground duels(%)"] = (
            100 * duels_total ["opp Ground duels won"] / duels_total[
        "opp Ground duels"]).round(1)
    duels_total ["opp Ground duels(%)"] = duels_total ["opp Ground duels(%)"].fillna(0)
    duels_total.drop(['opp Duels',"opp Aerial duels","opp Ground duels"],axis=1,inplace=True)
    interactive_table(duels_total.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    duels_mean=computeteamstats_on_games_mean[["Team",'Duels', 'Duels won',"Duels(%)",
   'Ground duels', 'Ground duels won',"Ground duels(%)", 'Aerial duels', 'Aerial duels won',"Aerial duels(%)",
   'Possession lost', 'Fouls', 'Was fouled',
    'opp Duels won',
     'opp Ground duels won',
     'opp Aerial duels won',
    'opp Possession lost', 'opp Fouls',"opp Duels(%)","opp Aerial duels(%)","opp Ground duels(%)"]]
    interactive_table(duels_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])


st.header("Passing Stats")
passingselectors=st.selectbox("Select Stat:",['Touches','Passes',
   'Crosses',  'Long balls',
   'Big chances created'])
total, pergame = st.tabs(['Total', 'Per Game'])
regex1 = "Team|" + passingselectors
with total:
    passing_total=computeteamstats_on_games_total.groupby('Team')[['Touches', 'Accurate passes', 'Total passes',
   'Key passes', 'Total Crosses', 'Accurate Crosses', 'Total Long balls',
   'Accurate Long balls', 'Big chances created', 'opp Touches', 'opp Accurate passes',
    'opp Total passes',
    'opp Key passes', 'opp Total Crosses',
    'opp Accurate Crosses', 'opp Total Long balls',
    'opp Accurate Long balls',
    'opp Big chances created']].sum().reset_index()
    passing_total["Passes(%)"] = (
                100 * passing_total["Accurate passes"] / passing_total[
            "Total passes"]).round(1)
    passing_total["Passes(%)"] = passing_total["Passes(%)"].fillna(0)
    passing_total["Crosses(%)"] = (
                100 * passing_total["Accurate Crosses"] / passing_total[
            "Total Crosses"]).round(1)
    passing_total["Crosses(%)"] = passing_total["Crosses(%)"].fillna(0)
    passing_total["Long balls(%)"] = (
                100 * passing_total["Accurate Long balls"] / passing_total[
            "Total Long balls"]).round(1)
    passing_total["Long balls(%)"] = passing_total["Long balls(%)"].fillna(0)
    passing_total["opp Passes(%)"] = (
            100 * passing_total["opp Accurate passes"] / passing_total[
        "opp Total passes"]).round(1)
    passing_total["opp Passes(%)"] = passing_total["opp Passes(%)"].fillna(0)
    passing_total["opp Crosses(%)"] = (
            100 * passing_total["opp Accurate Crosses"] / passing_total[
        "opp Total Crosses"]).round(1)
    passing_total["opp Crosses(%)"] = passing_total["opp Crosses(%)"].fillna(0)
    passing_total["opp Long balls(%)"] = (
            100 * passing_total["opp Accurate Long balls"] / passing_total[
        "opp Total Long balls"]).round(1)
    passing_total["opp Long balls(%)"] = passing_total["opp Long balls(%)"].fillna(0)
    passing_total=passing_total.rename(columns={ 'Accurate passes': 'Accurate Passes','Total passes':'Total Passes','Key passes':'Key Passes', 'opp Accurate passes':'opp Accurate Passes',
    'opp Total passes':'opp Total Passes','opp Key passes':'opp Key Passes'})
    interactive_table(passing_total.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    passing_mean=computeteamstats_on_games_mean[["Team",'Touches', 'Accurate passes', 'Total passes',
   'Key passes', 'Total Crosses', 'Accurate Crosses', 'Total Long balls',
   'Accurate Long balls', 'Big chances created', 'opp Touches', 'opp Accurate passes',
    'opp Total passes',
    'opp Key passes', 'opp Total Crosses',
    'opp Accurate Crosses', 'opp Total Long balls',
    'opp Accurate Long balls',
    'opp Big chances created',"Passes(%)","opp Passes(%)","Crosses(%)","opp Crosses(%)","Long balls(%)","opp Long balls(%)"]]
    interactive_table(passing_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.header("Goalkeeping Stats")
goalkeepingselectors=st.selectbox("Select Stat:",['Saves','Punches', 'Runs out','High claims','Penalties saved'])
total, pergame = st.tabs(['Total', 'Per Game'])
regex1 = "Team|" + goalkeepingselectors
with total:
    goalkeeping_total=computeteamstats_on_games_total.groupby('Team')[['Saves',
   'Punches', 'Runs out', 'Runs out succ', 'High claims',
   'Saves from inside box', 'Penalties saved','opp Saves',
   'opp Punches', 'opp Runs out',
   'opp Runs out succ',
   'opp High claims',
   'opp Saves from inside box',
   'opp Penalties saved']].sum().reset_index()
    goalkeeping_total["Runs out(%)"] = (
                100 * goalkeeping_total["Runs out succ"] / goalkeeping_total[
            "Runs out"]).round(1)
    goalkeeping_total["Runs out(%)"] = goalkeeping_total["Runs out(%)"].fillna(0)
    goalkeeping_total["opp Runs out(%)"] = (
                100 * goalkeeping_total["opp Runs out succ"] / goalkeeping_total[
            "opp Runs out"]).round(1)
    goalkeeping_total["opp Runs out(%)"] = goalkeeping_total["opp Runs out(%)"].fillna(0)
    goalkeeping_total=goalkeeping_total.rename(columns={ 'Accurate passes': 'Accurate Passes','Total passes':'Total Passes','Key passes':'Key Passes', 'opp Accurate passes':'opp Accurate Passes',
    'opp Total passes':'opp Total Passes','opp Key passes':'opp Key Passes'})
    interactive_table(goalkeeping_total.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    goalkeeping_mean=computeteamstats_on_games_mean[["Team",'Saves',
   'Punches', 'Runs out', 'Runs out succ', 'High claims',
   'Saves from inside box', 'Penalties saved','opp Saves',
   'opp Punches', 'opp Runs out',
   'opp Runs out succ',
   'opp High claims',
   'opp Saves from inside box',
   'opp Penalties saved',"Runs out(%)","opp Runs out(%)"]]
    interactive_table(goalkeeping_mean.filter(regex=regex1).set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
