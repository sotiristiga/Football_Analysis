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



st.set_page_config(layout='wide', page_title="Ratings")

dataset2223=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2223.csv")
dataset2324=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2324.csv")
dataset2425=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")
dataset=pd.concat([dataset2324,dataset2425,dataset2223])
selected_ha = st.sidebar.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
selected_season = st.sidebar.selectbox("Season:",['All','2022-2023',"2023-2024",'2024-2025'],index=3)
selected_phase = st.sidebar.selectbox("Phase:",['Regular Season', 'Play offs', 'Play out','All'],index=3)
selected_wl = st.sidebar.selectbox("Result:",['Win','Draw', 'Lose','All'],index=3)
selected_round = st.sidebar.selectbox("Round:",['First Round', 'Second Round', 'All'],index=2)


if "All" in selected_ha:
    selected_ha = ['Away', 'Home',]
    dataset_filter=dataset.loc[dataset['Home_Away'].isin(selected_ha)]
    select_ha=''
else:
    dataset_filter=dataset.loc[dataset['Home_Away']==selected_ha]
    select_ha = selected_ha

if "All" in selected_season:
    selected_season = ['2022-2023','2023-2024','2024-2025']
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
    selected_phase = ['Regular Season', 'Play offs', 'Play out']
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

games = dataset_filter['Player'].value_counts().reset_index().rename(columns={'count': 'Games'})
computeplayerstats_total = dataset_filter.groupby('Player')[['Minutes played',
                                                       'Goals', 'Assists', 'Yellow card', 'Red card',
                                                       'Shots on target',
                                                       'Shots off target', 'Shots blocked', 'Dribble attempts',
                                                       'Dribble attempts succ', 'Penalty won', 'Big chances missed',
                                                       'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                       'Clearances',
                                                       'Blocked shots', 'Interceptions', 'Total tackles',
                                                       'Dribbled past',
                                                       'Penalty committed', 'Own goals', 'Last man tackle',
                                                       'Error led to shot', 'Clearance off line',
                                                       'Error led to goal',
                                                       'Touches', 'Accurate passes', 'Total passes',
                                                       'Key passes', 'Total Crosses', 'Accurate Crosses',
                                                       'Total Long balls',
                                                       'Accurate Long balls', 'Big chances created', 'Duels',
                                                       'Duels won',
                                                       'Ground duels', 'Ground duels won', 'Aerial duels',
                                                       'Aerial duels won',
                                                       'Possession lost', 'Fouls', 'Was fouled', 'Offsides',
                                                       'Saves',
                                                       'Punches', 'Runs out', 'Runs out succ', 'High claims',
                                                       'Saves from inside box',
                                                       'Penalties saved']].sum().reset_index()
computeplayerstats_total["Dribble(%)"] = (
            100 * computeplayerstats_total["Dribble attempts succ"] / computeplayerstats_total["Dribble attempts"]).round(1)
computeplayerstats_total["Dribble(%)"] = computeplayerstats_total["Dribble(%)"].fillna(0)
computeplayerstats_total["Passes(%)"] = (
            100 * computeplayerstats_total["Accurate passes"] / computeplayerstats_total["Total passes"]).round(1)
computeplayerstats_total["Passes(%)"] = computeplayerstats_total["Passes(%)"].fillna(0)
computeplayerstats_total["Crosses(%)"] = (
            100 * computeplayerstats_total["Accurate Crosses"] / computeplayerstats_total["Total Crosses"]).round(1)
computeplayerstats_total["Crosses(%)"] = computeplayerstats_total["Crosses(%)"].fillna(0)
computeplayerstats_total["Long balls(%)"] = (
            100 * computeplayerstats_total["Accurate Long balls"] / computeplayerstats_total["Total Long balls"]).round(1)
computeplayerstats_total["Long balls(%)"] = computeplayerstats_total["Long balls(%)"].fillna(0)
computeplayerstats_total["Duels(%)"] = (100 * computeplayerstats_total["Duels won"] / computeplayerstats_total["Duels"]).round(1)
computeplayerstats_total["Duels(%)"] = computeplayerstats_total["Duels(%)"].fillna(0)
computeplayerstats_total["Aerial duels(%)"] = (
            100 * computeplayerstats_total["Aerial duels won"] / computeplayerstats_total["Aerial duels"]).round(1)
computeplayerstats_total["Aerial duels(%)"] = computeplayerstats_total["Aerial duels(%)"].fillna(0)
computeplayerstats_total["Ground duels(%)"] = (
            100 * computeplayerstats_total["Ground duels won"] / computeplayerstats_total["Ground duels"]).round(1)
computeplayerstats_total["Ground duels(%)"] = computeplayerstats_total["Ground duels(%)"].fillna(0)
computeplayerstats_total["Runs out(%)"] = (
            100 * computeplayerstats_total["Runs out succ"] / computeplayerstats_total["Runs out"]).round(1)
computeplayerstats_total["Runs out(%)"] = computeplayerstats_total["Runs out(%)"].fillna(0)
computeplayerstats_total = pd.merge(computeplayerstats_total, games)
computeplayerstats_mean = dataset_filter.groupby('Player')[['Minutes played',
                                                       'Goals', 'Assists', 'Yellow card', 'Red card',
                                                       'Shots on target',
                                                       'Shots off target', 'Shots blocked', 'Dribble attempts',
                                                       'Dribble attempts succ', 'Penalty won', 'Big chances missed',
                                                       'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                       'Clearances',
                                                       'Blocked shots', 'Interceptions', 'Total tackles',
                                                       'Dribbled past',
                                                       'Penalty committed', 'Own goals', 'Last man tackle',
                                                       'Error led to shot', 'Clearance off line',
                                                       'Error led to goal',
                                                       'Touches', 'Accurate passes', 'Total passes',
                                                       'Key passes', 'Total Crosses', 'Accurate Crosses',
                                                       'Total Long balls',
                                                       'Accurate Long balls', 'Big chances created', 'Duels',
                                                       'Duels won',
                                                       'Ground duels', 'Ground duels won', 'Aerial duels',
                                                       'Aerial duels won',
                                                       'Possession lost', 'Fouls', 'Was fouled', 'Offsides',
                                                       'Saves',
                                                       'Punches', 'Runs out', 'Runs out succ', 'High claims',
                                                       'Saves from inside box',
                                                       'Penalties saved']].mean().reset_index().round(1)
computeplayerstats_mean["Dribble(%)"] = (
            100 * computeplayerstats_mean["Dribble attempts succ"] / computeplayerstats_mean["Dribble attempts"]).round(1)
computeplayerstats_mean["Dribble(%)"] = computeplayerstats_mean["Dribble(%)"].fillna(0)
computeplayerstats_mean["Passes(%)"] = (
            100 * computeplayerstats_mean["Accurate passes"] / computeplayerstats_mean["Total passes"]).round(1)
computeplayerstats_mean["Passes(%)"] = computeplayerstats_mean["Passes(%)"].fillna(0)
computeplayerstats_mean["Crosses(%)"] = (
            100 * computeplayerstats_mean["Accurate Crosses"] / computeplayerstats_mean["Total Crosses"]).round(1)
computeplayerstats_mean["Crosses(%)"] = computeplayerstats_mean["Crosses(%)"].fillna(0)
computeplayerstats_mean["Long balls(%)"] = (
            100 * computeplayerstats_mean["Accurate Long balls"] / computeplayerstats_mean["Total Long balls"]).round(1)
computeplayerstats_mean["Long balls(%)"] = computeplayerstats_mean["Long balls(%)"].fillna(0)
computeplayerstats_mean["Duels(%)"] = (100 * computeplayerstats_mean["Duels won"] / computeplayerstats_mean["Duels"]).round(1)
computeplayerstats_mean["Duels(%)"] = computeplayerstats_mean["Duels(%)"].fillna(0)
computeplayerstats_mean["Aerial duels(%)"] = (
            100 * computeplayerstats_mean["Aerial duels won"] / computeplayerstats_mean["Aerial duels"]).round(1)
computeplayerstats_mean["Aerial duels(%)"] = computeplayerstats_mean["Aerial duels(%)"].fillna(0)
computeplayerstats_mean["Ground duels(%)"] = (
            100 * computeplayerstats_mean["Ground duels won"] / computeplayerstats_mean["Ground duels"]).round(1)
computeplayerstats_mean["Ground duels(%)"] = computeplayerstats_mean["Ground duels(%)"].fillna(0)
computeplayerstats_mean["Runs out(%)"] = (
            100 * computeplayerstats_mean["Runs out succ"] / computeplayerstats_mean["Runs out"]).round(1)
computeplayerstats_mean["Runs out(%)"] = computeplayerstats_mean["Runs out(%)"].fillna(0)
computeplayerstats_mean = pd.merge(computeplayerstats_mean, games)
colsplus = ['Assists', 'Shots on target', 'Shots off target', 'Shots blocked',
                'Dribble attempts succ', 'Dribble attempts', "Dribble(%)", 'Penalty won',
                'Clearances', 'Blocked shots', 'Interceptions', 'Total tackles', 'Last man tackle',
                'Clearance off line', 'Touches', 'Accurate passes', 'Total passes', "Passes(%)",
                'Key passes', 'Accurate Crosses', 'Total Crosses', "Crosses(%)", 'Accurate Long balls',
                'Total Long balls', "Long balls(%)",
                'Big chances created', 'Duels won', 'Duels', "Duels(%)", 'Ground duels won', 'Ground duels',
                "Ground duels(%)", 'Aerial duels won', 'Aerial duels', "Aerial duels(%)",
                'Was fouled']
colsminus = ['Red card', 'Big chances missed', 'Penalty miss', 'Hit woodwork', 'Dribbled past', 'Penalty committed',
             'Own goals', 'Error led to shot', 'Error led to goal', 'Possession lost',
             'Fouls', 'Offsides']
colplusgk=[ 'Punches', 'Runs out succ', 'Runs out', "Runs out(%)", 'High claims',
                'Saves from inside box', 'Penalties saved', 'Defensive actions']

computeplayerstats_mean_gk=computeplayerstats_mean[['Player','Saves', 'Punches', 'Runs out succ', 'Runs out', "Runs out(%)", 'High claims',
                'Saves from inside box', 'Penalties saved', 'Defensive actions']].dropna()

def player_rating_stat_higher(dataset,stat):
    dataset1=dataset[["Player",stat]].sort_values(stat).reset_index()
    dataset1.drop("index",axis=1,inplace=True)
    final_dataset=dataset1.reset_index() >> mutate(Rating=(100*(X.index+1)/X.Player.nunique()),Rating1=(100-(100-X.Rating.round(0))*0.5).round(0))
    final_dataset.rename(columns={'Rating1':'Rating '+ stat},inplace=True)
    final_dataset.drop(["index","Rating",stat],axis=1,inplace=True)
    return final_dataset

def player_rating_stat_lower(dataset,stat):
    dataset1=dataset[["Player",stat]].sort_values(stat,ascending=True).reset_index()
    dataset1.drop("index",axis=1,inplace=True)
    final_dataset=dataset1.reset_index() >> mutate(Rating=(100*(X.index+1)/X.Player.nunique()),Rating1=(100-(100-X.Rating.round(0))*0.5).round(0))
    final_dataset.rename(columns={'Rating1':'Rating '+ stat},inplace=True)
    final_dataset.drop(["index","Rating",stat],axis=1,inplace=True)
    return final_dataset

players_ratings1 = player_rating_stat_higher(computeplayerstats_mean, 'Goals')
for i in colsplus:
    df2 = player_rating_stat_higher(computeplayerstats_mean, i)
    players_ratings1 = pd.merge(players_ratings1, df2)

players_ratings2 = player_rating_stat_lower(computeplayerstats_mean, 'Yellow card')
for i in colsminus:
    df3 = player_rating_stat_lower(computeplayerstats_mean, i)
    players_ratings2 = pd.merge(players_ratings2, df3)

players_ratings = pd.merge(players_ratings1, players_ratings2)
players_ratingsgk = player_rating_stat_higher(computeplayerstats_mean_gk, 'Saves')
for i in colplusgk:
    df2 = player_rating_stat_higher(computeplayerstats_mean_gk, i)
    players_ratingsgk = pd.merge(players_ratingsgk, df2)

players_ratings=pd.merge(players_ratings,players_ratingsgk,how='left')
overall=players_ratings.melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Overall'})


attack=players_ratings[['Player', 'Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',
                 'Rating Dribble attempts', "Rating Dribble(%)", 'Rating Penalty won', 'Rating Big chances missed', 'Rating Penalty miss',
                 'Rating Hit woodwork', 'Rating Offsides','Rating Goals']].melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Attack'})
defense=players_ratings[['Player', 'Rating Defensive actions', 'Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
                 'Rating Dribbled past',
                 'Rating Penalty committed', 'Rating Own goals', 'Rating Last man tackle', 'Rating Error led to shot', 'Rating Clearance off line',
                 'Rating Error led to goal']].melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Defense'})
duels=players_ratings[['Player','Rating Duels', 'Rating Duels won',"Rating Duels(%)", 'Rating Ground duels', 'Rating Ground duels won','Rating Ground duels(%)', 'Rating Aerial duels',
                                'Rating Aerial duels won','Rating Aerial duels(%)','Rating Possession lost', 'Rating Fouls', 'Rating Was fouled']].melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Duels'})

passing=players_ratings[
                ['Player','Rating Touches', 'Rating Accurate passes', 'Rating Total passes', "Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses',
                 'Rating Total Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls', 'Rating Total Long balls', "Rating Long balls(%)",
                 'Rating Big chances created','Rating Assists']].melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Passing'})


goalkeeping=players_ratings[['Player','Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box',
                 'Rating Penalties saved']].melt(id_vars='Player').groupby('Player')['value'].mean().round(0).reset_index().rename(columns={'value':'Goalkeeping'})

finaldataset=pd.merge(attack,passing)
finaldataset=pd.merge(finaldataset,defense,on='Player')
finaldataset=pd.merge(finaldataset,duels)
finaldataset=pd.merge(finaldataset,goalkeeping)
finaldataset=pd.merge(finaldataset,overall)

interactive_table(finaldataset.round(0).set_index('Player').sort_values('Overall',ascending=False),
                      paging=False, height=900, width=4000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
