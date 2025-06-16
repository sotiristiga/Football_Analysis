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
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n, sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
from itables.streamlit import interactive_table
from itables import to_html_datatable
from streamlit.components.v1 import html
from plotly.subplots import make_subplots

st.set_page_config(layout='wide', page_title="Search stats from each team")

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
  * ## [Players Stats](#players-stats)  
  * ## [Stats by game](#stats-by-game)
''', unsafe_allow_html=True)

def ha_against_format(HA):
    if HA == "A":
        return "H"
    elif HA == "H":
        return "A"
dataset["HA1"] = dataset['Home_Away'].apply(ha_against_format)
st.header("Filters")
f1,f2,f3,f4,f5,f6=st.columns(6)

with f2:
    selected_season = st.selectbox("Season:", ['All', '2022-2023', '2023-2024', '2024-2025'], index=3)
with f3:
    selected_phase = st.selectbox("Phase:", ['Regular Season', 'Play offs', "Play In", 'Play out', 'All'], index=4)
with f4:
    selected_round = st.selectbox("Round:", ['First Round', 'Second Round', 'All'], index=2)
with f5:
    selected_ha = st.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
with f6:
    selected_wl = st.selectbox("Result:",['Win','Draw', 'Lose','All'],index=3)

if "All" in selected_ha:
    selected_ha = ['Away', 'Home' ]
    dataset_filter1 = dataset.loc[dataset['Home_Away'].isin(selected_ha)]
    dataset_filter2 = dataset.loc[dataset['HA1'].isin(selected_ha)]
    select_ha = ''
elif selected_ha=="Home":
    dataset_filter1 = dataset.loc[dataset['Home_Away'] =="Home"]
    dataset_filter2 = dataset.loc[dataset['Home_Away'] == "Away"]
    select_ha = selected_ha
elif selected_ha=="Away":
    dataset_filter2 = dataset.loc[dataset['Home_Away'] =="Home"]
    dataset_filter1 = dataset.loc[dataset['Home_Away'] == "Away"]
    select_ha = selected_ha

if "All" in selected_season:
    selected_season = ['2022-2023',
                       '2023-2024', '2024-2025']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Season'].isin(selected_season)]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Season'].isin(selected_season)]
    select_season = ''
else:
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Season'] == selected_season]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Season'] == selected_season]
    select_season = selected_season

if "All" in selected_wl:
    selected_wl = ['Win', 'Draw', 'Lose']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Result'].isin(selected_wl)]
    select_wl = ''
elif selected_wl=='Win':
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Result'] == 'Win']
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Result'] == 'Lose']
    select_wl = selected_wl

elif selected_wl=='Lose':
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Result'] == 'Lose']
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Result'] == 'Win']
    select_wl = selected_wl

elif selected_wl=='Draw':
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Result'] == 'Draw']
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Result'] == 'Draw']
    select_wl = selected_wl

if "All" in selected_phase:
    selected_phase = ['Regular Season', 'Play offs', "Play In",'Play out']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Phase'].isin(selected_phase)]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Phase'].isin(selected_phase)]
    select_phase = ''
else:
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Phase'] == selected_phase]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Phase'] == selected_phase]
    select_phase = selected_phase

if "All" in selected_round:
    selected_round = ['First Round', 'Second Round']
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Round'].isin(selected_round)]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Round'].isin(selected_round)]
    select_round = ''
else:
    dataset_filter1 = dataset_filter1.loc[dataset_filter1['Round'] == selected_round]
    dataset_filter2 = dataset_filter2.loc[dataset_filter2['Round'] == selected_round]
    select_round = selected_round


with f1:
    selected_Team = st.selectbox("Team:", dataset_filter1['Team'].reset_index().sort_values('Team')['Team'].unique())


def computeteamstats(dataset1,dataset2, Team_Select):
    computeTeamstats_on_games = dataset1.groupby(["idseason", 'Team'])[[
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
    computeTeamstats_on_games["Dribble(%)"] = (
                100 * computeTeamstats_on_games["Dribble attempts succ"] / computeTeamstats_on_games[
            "Dribble attempts"]).round(1)
    computeTeamstats_on_games["Dribble(%)"] = computeTeamstats_on_games["Dribble(%)"].fillna(0)
    computeTeamstats_on_games["Passes(%)"] = (
                100 * computeTeamstats_on_games["Accurate passes"] / computeTeamstats_on_games["Total passes"]).round(1)
    computeTeamstats_on_games["Passes(%)"] = computeTeamstats_on_games["Passes(%)"].fillna(0)
    computeTeamstats_on_games["Crosses(%)"] = (
                100 * computeTeamstats_on_games["Accurate Crosses"] / computeTeamstats_on_games["Total Crosses"]).round(
        1)
    computeTeamstats_on_games["Crosses(%)"] = computeTeamstats_on_games["Crosses(%)"].fillna(0)
    computeTeamstats_on_games["Long balls(%)"] = (
                100 * computeTeamstats_on_games["Accurate Long balls"] / computeTeamstats_on_games[
            "Total Long balls"]).round(1)
    computeTeamstats_on_games["Long balls(%)"] = computeTeamstats_on_games["Long balls(%)"].fillna(0)
    computeTeamstats_on_games["Duels(%)"] = (
                100 * computeTeamstats_on_games["Duels won"] / computeTeamstats_on_games["Duels"]).round(1)
    computeTeamstats_on_games["Duels(%)"] = computeTeamstats_on_games["Duels(%)"].fillna(0)
    computeTeamstats_on_games["Aerial duels(%)"] = (
                100 * computeTeamstats_on_games["Aerial duels won"] / computeTeamstats_on_games["Aerial duels"]).round(
        1)
    computeTeamstats_on_games["Aerial duels(%)"] = computeTeamstats_on_games["Aerial duels(%)"].fillna(0)
    computeTeamstats_on_games["Ground duels(%)"] = (
                100 * computeTeamstats_on_games["Ground duels won"] / computeTeamstats_on_games["Ground duels"]).round(
        1)
    computeTeamstats_on_games["Ground duels(%)"] = computeTeamstats_on_games["Ground duels(%)"].fillna(0)
    computeTeamstats_on_games["Runs out(%)"] = (
                100 * computeTeamstats_on_games["Runs out succ"] / computeTeamstats_on_games["Runs out"]).round(1)
    computeTeamstats_on_games["Runs out(%)"] = computeTeamstats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = dataset2.groupby(['idseason', 'Against'])[[
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
    computeAgainststats_on_games["Dribble(%)"] = (
                100 * computeAgainststats_on_games["Dribble attempts succ"] / computeAgainststats_on_games[
            "Dribble attempts"]).round(1)
    computeAgainststats_on_games["Dribble(%)"] = computeAgainststats_on_games["Dribble(%)"].fillna(0)
    computeAgainststats_on_games["Passes(%)"] = (
                100 * computeAgainststats_on_games["Accurate passes"] / computeAgainststats_on_games[
            "Total passes"]).round(1)
    computeAgainststats_on_games["Passes(%)"] = computeAgainststats_on_games["Passes(%)"].fillna(0)
    computeAgainststats_on_games["Crosses(%)"] = (
                100 * computeAgainststats_on_games["Accurate Crosses"] / computeAgainststats_on_games[
            "Total Crosses"]).round(1)
    computeAgainststats_on_games["Crosses(%)"] = computeAgainststats_on_games["Crosses(%)"].fillna(0)
    computeAgainststats_on_games["Long balls(%)"] = (
                100 * computeAgainststats_on_games["Accurate Long balls"] / computeAgainststats_on_games[
            "Total Long balls"]).round(1)
    computeAgainststats_on_games["Long balls(%)"] = computeAgainststats_on_games["Long balls(%)"].fillna(0)
    computeAgainststats_on_games["Duels(%)"] = (
                100 * computeAgainststats_on_games["Duels won"] / computeAgainststats_on_games["Duels"]).round(1)
    computeAgainststats_on_games["Duels(%)"] = computeAgainststats_on_games["Duels(%)"].fillna(0)
    computeAgainststats_on_games["Aerial duels(%)"] = (
                100 * computeAgainststats_on_games["Aerial duels won"] / computeAgainststats_on_games[
            "Aerial duels"]).round(1)
    computeAgainststats_on_games["Aerial duels(%)"] = computeAgainststats_on_games["Aerial duels(%)"].fillna(0)
    computeAgainststats_on_games["Ground duels(%)"] = (
                100 * computeAgainststats_on_games["Ground duels won"] / computeAgainststats_on_games[
            "Ground duels"]).round(1)
    computeAgainststats_on_games["Ground duels(%)"] = computeAgainststats_on_games["Ground duels(%)"].fillna(0)
    computeAgainststats_on_games["Runs out(%)"] = (
                100 * computeAgainststats_on_games["Runs out succ"] / computeAgainststats_on_games["Runs out"]).round(1)
    computeAgainststats_on_games["Runs out(%)"] = computeAgainststats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = computeAgainststats_on_games.add_prefix('opp ').rename(
        columns={'opp Against': 'Team', 'opp idseason': 'idseason'})

    computeteamstats_on_games_total = pd.merge(computeTeamstats_on_games, computeAgainststats_on_games,
                                               on=['Team', 'idseason'])

    computeteamstats_on_games_mean = computeteamstats_on_games_total.groupby('Team')[
        ['Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
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
         'opp Goals', 'opp Assists', 'opp Yellow card', 'opp Red card', 'opp Shots on target',
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

    computeteamstats_on_games_mean["Dribble(%)"] = (
                100 * computeteamstats_on_games_mean["Dribble attempts succ"] / computeteamstats_on_games_mean[
            "Dribble attempts"]).round(1)
    computeteamstats_on_games_mean["Dribble(%)"] = computeteamstats_on_games_mean["Dribble(%)"].fillna(0)
    computeteamstats_on_games_mean["Passes(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate passes"] / computeteamstats_on_games_mean[
            "Total passes"]).round(1)
    computeteamstats_on_games_mean["Passes(%)"] = computeteamstats_on_games_mean["Passes(%)"].fillna(0)
    computeteamstats_on_games_mean["Crosses(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate Crosses"] / computeteamstats_on_games_mean[
            "Total Crosses"]).round(1)
    computeteamstats_on_games_mean["Crosses(%)"] = computeteamstats_on_games_mean["Crosses(%)"].fillna(0)
    computeteamstats_on_games_mean["Long balls(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate Long balls"] / computeteamstats_on_games_mean[
            "Total Long balls"]).round(1)
    computeteamstats_on_games_mean["Long balls(%)"] = computeteamstats_on_games_mean["Long balls(%)"].fillna(0)
    computeteamstats_on_games_mean["Duels(%)"] = (
                100 * computeteamstats_on_games_mean["Duels won"] / computeteamstats_on_games_mean["Duels"]).round(1)
    computeteamstats_on_games_mean["Duels(%)"] = computeteamstats_on_games_mean["Duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Aerial duels(%)"] = (
                100 * computeteamstats_on_games_mean["Aerial duels won"] / computeteamstats_on_games_mean[
            "Aerial duels"]).round(1)
    computeteamstats_on_games_mean["Aerial duels(%)"] = computeteamstats_on_games_mean["Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Ground duels(%)"] = (
                100 * computeteamstats_on_games_mean["Ground duels won"] / computeteamstats_on_games_mean[
            "Ground duels"]).round(1)
    computeteamstats_on_games_mean["Ground duels(%)"] = computeteamstats_on_games_mean["Ground duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Runs out(%)"] = (
                100 * computeteamstats_on_games_mean["Runs out succ"] / computeteamstats_on_games_mean[
            "Runs out"]).round(1)
    computeteamstats_on_games_mean["Runs out(%)"] = computeteamstats_on_games_mean["Runs out(%)"].fillna(0)

    computeteamstats_on_games_mean["opp Dribble(%)"] = (
                100 * computeteamstats_on_games_mean["opp Dribble attempts succ"] / computeteamstats_on_games_mean[
            "opp Dribble attempts"]).round(1)
    computeteamstats_on_games_mean["opp Dribble(%)"] = computeteamstats_on_games_mean["opp Dribble(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Passes(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate passes"] / computeteamstats_on_games_mean[
            "opp Total passes"]).round(1)
    computeteamstats_on_games_mean["opp Passes(%)"] = computeteamstats_on_games_mean["opp Passes(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Crosses(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate Crosses"] / computeteamstats_on_games_mean[
            "opp Total Crosses"]).round(1)
    computeteamstats_on_games_mean["opp Crosses(%)"] = computeteamstats_on_games_mean["opp Crosses(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Long balls(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate Long balls"] / computeteamstats_on_games_mean[
            "opp Total Long balls"]).round(1)
    computeteamstats_on_games_mean["opp Long balls(%)"] = computeteamstats_on_games_mean["opp Long balls(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Duels won"] / computeteamstats_on_games_mean[
            "opp Duels"]).round(1)
    computeteamstats_on_games_mean["opp Duels(%)"] = computeteamstats_on_games_mean["opp Duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Ground duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Ground duels won"] / computeteamstats_on_games_mean[
            "opp Ground duels"]).round(1)
    computeteamstats_on_games_mean["opp Ground duels(%)"] = computeteamstats_on_games_mean[
        "opp Ground duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Aerial duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Aerial duels won"] / computeteamstats_on_games_mean[
            "opp Aerial duels"]).round(1)
    computeteamstats_on_games_mean["opp Aerial duels(%)"] = computeteamstats_on_games_mean[
        "opp Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Runs out(%)"] = (
                100 * computeteamstats_on_games_mean["opp Runs out succ"] / computeteamstats_on_games_mean[
            "opp Runs out"]).round(1)
    computeteamstats_on_games_mean["opp Runs out(%)"] = computeteamstats_on_games_mean["opp Runs out(%)"].fillna(0)
    computeteamstats_on_games_sum = computeteamstats_on_games_total.groupby('Team')[
        ['Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
         'Shots off target', 'Shots blocked', 'Dribble attempts',
         'Dribble attempts succ', 'Penalty won', 'Big chances missed',
         'Penalty miss', 'Hit woodwork', 'Defensive actions', 'Clearances',
         'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
         'Penalty committed', 'Own goals', 'Last man tackle',
         'Error led to shot', 'Clearance off line', 'Error led to goal',
         'Touches', 'Accurate passes', 'Total passes',
         'Key passes', 'Total Crosses', 'Accurate Crosses',
         'Total Long balls',
         'Accurate Long balls', 'Big chances created', 'Duels', 'Duels won',
         'Ground duels', 'Ground duels won', 'Aerial duels',
         'Aerial duels won',
         'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
         'Punches', 'Runs out', 'Runs out succ', 'High claims',
         'Saves from inside box', 'Penalties saved',
         'opp Goals', 'opp Assists', 'opp Yellow card', 'opp Red card',
         'opp Shots on target',
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
         'opp Penalties saved']].sum().reset_index().round(1)

    computeteamstats_on_games_sum["Dribble(%)"] = (
            100 * computeteamstats_on_games_sum["Dribble attempts succ"] / computeteamstats_on_games_sum[
        "Dribble attempts"]).round(1)
    computeteamstats_on_games_sum["Dribble(%)"] = computeteamstats_on_games_sum["Dribble(%)"].fillna(0)
    computeteamstats_on_games_sum["Passes(%)"] = (
            100 * computeteamstats_on_games_sum["Accurate passes"] / computeteamstats_on_games_sum[
        "Total passes"]).round(1)
    computeteamstats_on_games_sum["Passes(%)"] = computeteamstats_on_games_sum["Passes(%)"].fillna(0)
    computeteamstats_on_games_sum["Crosses(%)"] = (
            100 * computeteamstats_on_games_sum["Accurate Crosses"] / computeteamstats_on_games_sum[
        "Total Crosses"]).round(1)
    computeteamstats_on_games_sum["Crosses(%)"] = computeteamstats_on_games_sum["Crosses(%)"].fillna(0)
    computeteamstats_on_games_sum["Long balls(%)"] = (
            100 * computeteamstats_on_games_sum["Accurate Long balls"] / computeteamstats_on_games_sum[
        "Total Long balls"]).round(1)
    computeteamstats_on_games_sum["Long balls(%)"] = computeteamstats_on_games_sum["Long balls(%)"].fillna(0)
    computeteamstats_on_games_sum["Duels(%)"] = (
            100 * computeteamstats_on_games_sum["Duels won"] / computeteamstats_on_games_sum["Duels"]).round(1)
    computeteamstats_on_games_sum["Duels(%)"] = computeteamstats_on_games_sum["Duels(%)"].fillna(0)
    computeteamstats_on_games_sum["Aerial duels(%)"] = (
            100 * computeteamstats_on_games_sum["Aerial duels won"] / computeteamstats_on_games_sum[
        "Aerial duels"]).round(1)
    computeteamstats_on_games_sum["Aerial duels(%)"] = computeteamstats_on_games_sum["Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_sum["Ground duels(%)"] = (
            100 * computeteamstats_on_games_sum["Ground duels won"] / computeteamstats_on_games_sum[
        "Ground duels"]).round(1)
    computeteamstats_on_games_sum["Ground duels(%)"] = computeteamstats_on_games_sum["Ground duels(%)"].fillna(0)
    computeteamstats_on_games_sum["Runs out(%)"] = (
            100 * computeteamstats_on_games_sum["Runs out succ"] / computeteamstats_on_games_sum[
        "Runs out"]).round(1)
    computeteamstats_on_games_sum["Runs out(%)"] = computeteamstats_on_games_sum["Runs out(%)"].fillna(0)

    computeteamstats_on_games_sum["opp Dribble(%)"] = (
            100 * computeteamstats_on_games_sum["opp Dribble attempts succ"] / computeteamstats_on_games_sum[
        "opp Dribble attempts"]).round(1)
    computeteamstats_on_games_sum["opp Dribble(%)"] = computeteamstats_on_games_sum["opp Dribble(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Passes(%)"] = (
            100 * computeteamstats_on_games_sum["opp Accurate passes"] / computeteamstats_on_games_sum[
        "opp Total passes"]).round(1)
    computeteamstats_on_games_sum["opp Passes(%)"] = computeteamstats_on_games_sum["opp Passes(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Crosses(%)"] = (
            100 * computeteamstats_on_games_sum["opp Accurate Crosses"] / computeteamstats_on_games_sum[
        "opp Total Crosses"]).round(1)
    computeteamstats_on_games_sum["opp Crosses(%)"] = computeteamstats_on_games_sum["opp Crosses(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Long balls(%)"] = (
            100 * computeteamstats_on_games_sum["opp Accurate Long balls"] / computeteamstats_on_games_sum[
        "opp Total Long balls"]).round(1)
    computeteamstats_on_games_sum["opp Long balls(%)"] = computeteamstats_on_games_sum["opp Long balls(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Duels(%)"] = (
            100 * computeteamstats_on_games_sum["opp Duels won"] / computeteamstats_on_games_sum[
        "opp Duels"]).round(1)
    computeteamstats_on_games_sum["opp Duels(%)"] = computeteamstats_on_games_sum["opp Duels(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Ground duels(%)"] = (
            100 * computeteamstats_on_games_sum["opp Ground duels won"] / computeteamstats_on_games_sum[
        "opp Ground duels"]).round(1)
    computeteamstats_on_games_sum["opp Ground duels(%)"] = computeteamstats_on_games_sum[
        "opp Ground duels(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Aerial duels(%)"] = (
            100 * computeteamstats_on_games_sum["opp Aerial duels won"] / computeteamstats_on_games_sum[
        "opp Aerial duels"]).round(1)
    computeteamstats_on_games_sum["opp Aerial duels(%)"] = computeteamstats_on_games_sum[
        "opp Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_sum["opp Runs out(%)"] = (
            100 * computeteamstats_on_games_sum["opp Runs out succ"] / computeteamstats_on_games_sum[
        "opp Runs out"]).round(1)
    computeteamstats_on_games_sum["opp Runs out(%)"] = computeteamstats_on_games_sum["opp Runs out(%)"].fillna(0)
    computeteamstats_on_games_sum = computeteamstats_on_games_sum.loc[computeteamstats_on_games_sum.Team == Team_Select]
    computeteamstats_on_games_mean = computeteamstats_on_games_mean.loc[
        computeteamstats_on_games_mean.Team == Team_Select]
    computeteamstats_on_games_sum['Team'] = computeteamstats_on_games_sum[
                                                'Team'] + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl
    computeteamstats_on_games_mean['Team'] = computeteamstats_on_games_mean[
                                                 'Team'] + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl
    return [computeteamstats_on_games_sum, computeteamstats_on_games_mean]


teamssums = computeteamstats(dataset_filter1, dataset_filter2,selected_Team)[0]
teamswins = computeteamstats(dataset_filter1, dataset_filter2, selected_Team)[1]
st.write('## Team: ' + selected_Team)

st.write('### Basic Stats')
total, pergame = st.tabs(['Total', 'Per Game'])

with total:
    basic_total = teamssums[
        ['Team', "Goals", "opp Goals", 'Assists', 'opp Assists', 'Yellow card', 'opp Yellow card', 'Red card',
         'opp Red card']]
    interactive_table(basic_total.set_index('Team'),
                      paging=False, height=900, width=100, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=600, fixedHeader=True, scroller=True, filter='left',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    basic_mean = teamswins[
        ["Team", "Goals", "opp Goals", 'Assists', 'opp Assists', 'Yellow card', 'opp Yellow card', 'Red card',
         'opp Red card']]
    interactive_table(basic_mean.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('### Attack Stats')
total, pergame = st.tabs(['Total', 'Per Game'])

with total:
    attack_total = teamssums[
        ['Team', 'Shots on target', 'opp Shots on target', 'Shots off target', 'opp Shots off target',
         'Shots blocked', 'opp Shots blocked', 'Dribble attempts succ', 'opp Dribble attempts succ',
         'Dribble attempts', 'opp Dribble attempts', "Dribble(%)", "Dribble(%)", 'Penalty won', 'opp Penalty won',
         'Big chances missed', 'opp Big chances missed', 'Penalty miss', 'opp Penalty miss',
         'Hit woodwork', 'opp Hit woodwork', 'Offsides', 'opp Offsides']]

    interactive_table(attack_total.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    attack_mean = teamswins[
        ["Team", 'Shots on target', 'opp Shots on target', 'Shots off target', 'opp Shots off target',
         'Shots blocked', 'opp Shots blocked', 'Dribble attempts succ', 'opp Dribble attempts succ', "Dribble(%)",
         "opp Dribble(%)",
         'Dribble attempts', 'opp Dribble attempts', 'Penalty won', 'opp Penalty won', 'Big chances missed',
         'opp Big chances missed', 'Penalty miss', 'opp Penalty miss',
         'Hit woodwork', 'opp Hit woodwork', 'Offsides', 'opp Offsides']]
    interactive_table(attack_mean.set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write("### Defence Stats")
total, pergame = st.tabs(['Total', 'Per Game'])
with total:
    defence_total = teamssums[['Team', 'Defensive actions', 'opp Defensive actions', 'Clearances', 'opp Clearances',
                               'Blocked shots', 'opp Blocked shots', 'Interceptions', 'opp Interceptions',
                               'Total tackles', 'opp Total tackles', 'Dribbled past', 'opp Dribbled past',
                               'Penalty committed', 'opp Penalty committed', 'Own goals', 'opp Own goals',
                               'Last man tackle', 'opp Last man tackle',
                               'Error led to shot', 'opp Error led to shot', 'Clearance off line',
                               'opp Clearance off line', 'Error led to goal', 'opp Error led to goal']]
    interactive_table(defence_total.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    defence_mean = teamswins[["Team", 'Defensive actions', 'Clearances',
                              'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
                              'Penalty committed', 'Own goals', 'Last man tackle',
                              'Error led to shot', 'Clearance off line', 'Error led to goal', 'opp Defensive actions',
                              'opp Clearances',
                              'opp Blocked shots', 'opp Interceptions',
                              'opp Total tackles', 'opp Dribbled past',
                              'opp Penalty committed', 'opp Own goals',
                              'opp Last man tackle',
                              'opp Error led to shot',
                              'opp Clearance off line',
                              'opp Error led to goal']]
    interactive_table(defence_mean.set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('### Duels Stats')
total, pergame = st.tabs(['Total', 'Per Game'])

with total:
    duels_total = teamssums[['Team', 'Duels', 'Duels won', "Duels(%)", 'opp Duels',
                             'opp Duels won', "opp Duels(%)", 'Ground duels', 'Ground duels won', "Ground duels(%)",
                             'opp Ground duels won', "opp Ground duels(%)",
                             'Aerial duels', 'Aerial duels won', "Aerial duels(%)", 'opp Aerial duels won',
                             "opp Aerial duels(%)", 'Possession lost', 'opp Possession lost',
                             'Fouls', 'Was fouled']]

    interactive_table(duels_total.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    duels_mean = teamswins[["Team", 'Duels', 'Duels won', "Duels(%)", 'opp Duels',
                            'opp Duels won', "opp Duels(%)", 'Ground duels', 'Ground duels won', "Ground duels(%)",
                            'opp Ground duels won', "opp Ground duels(%)",
                            'Aerial duels', 'Aerial duels won', "Aerial duels(%)", 'opp Aerial duels won',
                            "opp Aerial duels(%)", 'Possession lost', 'opp Possession lost',
                            'Fouls', 'Was fouled']]
    interactive_table(duels_mean.set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
st.write('### Passing Stats')
total, pergame = st.tabs(['Total', 'Per Game'])
with total:
    passing_total = teamssums[["Team", 'Touches', 'opp Touches', 'Accurate passes', 'Total passes', "Passes(%)",
                               'opp Accurate passes', 'opp Total passes', "opp Passes(%)", 'Key passes',
                               'opp Key passes',
                               'Total Crosses', 'Accurate Crosses', "Crosses(%)", 'opp Total Crosses',
                               'opp Accurate Crosses', "opp Crosses(%)",
                               'Total Long balls', 'Accurate Long balls', "Long balls(%)", 'opp Total Long balls',
                               'opp Accurate Long balls', "opp Long balls(%)",
                               'Big chances created', 'opp Big chances created']]

    interactive_table(passing_total.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    passing_mean = teamswins[["Team", 'Touches', 'opp Touches', 'Accurate passes', 'Total passes', "Passes(%)",
                              'opp Accurate passes', 'opp Total passes', "opp Passes(%)", 'Key passes',
                              'opp Key passes',
                              'Total Crosses', 'Accurate Crosses', "Crosses(%)", 'opp Total Crosses',
                              'opp Accurate Crosses', "opp Crosses(%)",
                              'Total Long balls', 'Accurate Long balls', "Long balls(%)", 'opp Total Long balls',
                              'opp Accurate Long balls', "opp Long balls(%)",
                              'Big chances created', 'opp Big chances created']]
    interactive_table(passing_mean.set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('### Goalkeeping Stats')
total, pergame = st.tabs(['Total', 'Per Game'])
with total:
    goalkeeping_total = teamssums[['Team', 'Saves', 'opp Saves',
                                   'Punches', 'opp Punches', 'Runs out', 'Runs out succ', "Runs out(%)", 'opp Runs out',
                                   'opp Runs out succ', "opp Runs out(%)",
                                   'High claims', 'opp High claims', 'Saves from inside box',
                                   'opp Saves from inside box', 'Penalties saved', 'opp Penalties saved']]

    interactive_table(goalkeeping_total.set_index('Team'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
with pergame:
    goalkeeping_mean = teamswins[['Team', 'Saves', 'opp Saves',
                                  'Punches', 'opp Punches', 'Runs out', 'Runs out succ', "Runs out(%)", 'opp Runs out',
                                  'opp Runs out succ', "opp Runs out(%)",
                                  'High claims', 'opp High claims', 'Saves from inside box',
                                  'opp Saves from inside box', 'Penalties saved', 'opp Penalties saved']]
    interactive_table(goalkeeping_mean.set_index('Team'),
                      paging=False, height=900, width=500, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('### Players Stats')
games = dataset_filter[['Player','Team']].value_counts().reset_index().rename(columns={'count': 'Games'})
playersteamstotal,playersteamspergame=st.tabs(['Total','Per Game'])
with playersteamstotal:
    computeplayerstats_total = dataset_filter.groupby(['Player','Team'])[['Minutes played',
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
    computeplayerstats_total["Ground duels(%)"] = (
            100 * computeplayerstats_total["Ground duels won"] / computeplayerstats_total["Ground duels"]).round(1)
    computeplayerstats_total["Ground duels(%)"] = computeplayerstats_total["Ground duels(%)"].fillna(0)
    computeplayerstats_total["Aerial duels(%)"] = (
                100 * computeplayerstats_total["Aerial duels won"] / computeplayerstats_total["Aerial duels"]).round(1)
    computeplayerstats_total["Aerial duels(%)"] = computeplayerstats_total["Aerial duels(%)"].fillna(0)
    computeplayerstats_total["Runs out(%)"] = (
                100 * computeplayerstats_total["Runs out succ"] / computeplayerstats_total["Runs out"]).round(1)
    computeplayerstats_total["Runs out(%)"] = computeplayerstats_total["Runs out(%)"].fillna(0)

    computeplayerstats_total = pd.merge(computeplayerstats_total, games)
    teamstats_total=computeplayerstats_total.loc[computeplayerstats_total.Team==selected_Team][['Player','Games','Minutes played',
                                                           'Goals', 'Assists', 'Yellow card', 'Red card',
                                                           'Shots on target',
                                                           'Shots off target', 'Shots blocked', 'Dribble attempts succ','Dribble attempts',
                                                           "Dribble(%)", 'Penalty won', 'Big chances missed',
                                                           'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                           'Clearances',
                                                           'Blocked shots', 'Interceptions', 'Total tackles',
                                                           'Dribbled past',
                                                           'Penalty committed', 'Own goals', 'Last man tackle',
                                                           'Error led to shot', 'Clearance off line',
                                                           'Error led to goal',
                                                           'Touches', 'Accurate passes', 'Total passes',"Passes(%)",
                                                           'Key passes', 'Accurate Crosses','Total Crosses', "Crosses(%)",
                                                           'Accurate Long balls','Total Long balls',"Long balls(%)", 'Big chances created', 'Duels won','Duels',"Duels(%)",
                                                           'Ground duels won','Ground duels', "Ground duels(%)", 'Aerial duels won','Aerial duels',"Aerial duels(%)",
                                                           'Possession lost', 'Fouls', 'Was fouled', 'Offsides','Saves',
                                                           'Punches', 'Runs out succ','Runs out',  "Runs out(%)",'High claims','Saves from inside box','Penalties saved']]
    interactive_table(
        teamstats_total.sort_values('Minutes played',ascending=False).set_index('Player'),
        paging=False, height=900, width=2000, showIndex=True,
        classes="display order-column nowrap table_with_monospace_font", searching=True,
        fixedColumns=True, select=True, info=False, scrollCollapse=True,
        scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
        columnDefs=[{"className": "dt-center", "targets": "_all"}])
with playersteamspergame:
    computeplayerstats_mean = dataset_filter.groupby(['Player','Team'])[['Minutes played',
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
    computeplayerstats_mean["Ground duels(%)"] = (
            100 * computeplayerstats_mean["Ground duels won"] / computeplayerstats_mean["Ground duels"]).round(1)
    computeplayerstats_mean["Ground duels(%)"] = computeplayerstats_mean["Ground duels(%)"].fillna(0)
    computeplayerstats_mean["Aerial duels(%)"] = (
                100 * computeplayerstats_mean["Aerial duels won"] / computeplayerstats_mean["Aerial duels"]).round(1)
    computeplayerstats_mean["Aerial duels(%)"] = computeplayerstats_mean["Aerial duels(%)"].fillna(0)
    computeplayerstats_mean["Runs out(%)"] = (
                100 * computeplayerstats_mean["Runs out succ"] / computeplayerstats_mean["Runs out"]).round(1)
    computeplayerstats_mean["Runs out(%)"] = computeplayerstats_mean["Runs out(%)"].fillna(0)
    computeplayerstats_mean = pd.merge(computeplayerstats_mean, games)
    teamstats_mean=computeplayerstats_mean.loc[computeplayerstats_mean.Team==selected_Team][['Player','Games','Minutes played',
                                                           'Goals', 'Assists', 'Yellow card', 'Red card',
                                                           'Shots on target',
                                                           'Shots off target', 'Shots blocked', 'Dribble attempts succ','Dribble attempts',
                                                           "Dribble(%)", 'Penalty won', 'Big chances missed',
                                                           'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                           'Clearances',
                                                           'Blocked shots', 'Interceptions', 'Total tackles',
                                                           'Dribbled past',
                                                           'Penalty committed', 'Own goals', 'Last man tackle',
                                                           'Error led to shot', 'Clearance off line',
                                                           'Error led to goal',
                                                           'Touches', 'Accurate passes', 'Total passes',"Passes(%)",
                                                           'Key passes', 'Accurate Crosses','Total Crosses', "Crosses(%)",
                                                           'Accurate Long balls','Total Long balls',"Long balls(%)", 'Big chances created', 'Duels won','Duels',"Duels(%)",
                                                           'Ground duels won','Ground duels', "Ground duels(%)", 'Aerial duels won','Aerial duels',"Aerial duels(%)",
                                                           'Possession lost', 'Fouls', 'Was fouled', 'Offsides','Saves',
                                                           'Punches', 'Runs out succ','Runs out',  "Runs out(%)",'High claims','Saves from inside box','Penalties saved']]
    interactive_table(teamstats_mean.sort_values('Minutes played',ascending=False).set_index('Player'),
        paging=False, height=900, width=2000, showIndex=True,
        classes="display order-column nowrap table_with_monospace_font", searching=True,
        fixedColumns=True, select=True, info=False, scrollCollapse=True,
        scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
        columnDefs=[{"className": "dt-center", "targets": "_all"}])

st.write('### Stats by game')
try:


    computeTeamstats_on_games = dataset_filter.groupby(
        ["idseason", 'Team', 'Against', 'Home_Away', 'Result', 'Season', 'Phase', 'Round', 'Fixture'])[[
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
    computeTeamstats_on_games["Dribble(%)"] = (
                100 * computeTeamstats_on_games["Dribble attempts succ"] / computeTeamstats_on_games[
            "Dribble attempts"]).round(1)
    computeTeamstats_on_games["Dribble(%)"] = computeTeamstats_on_games["Dribble(%)"].fillna(0)
    computeTeamstats_on_games["Passes(%)"] = (
                100 * computeTeamstats_on_games["Accurate passes"] / computeTeamstats_on_games[
            "Total passes"]).round(1)
    computeTeamstats_on_games["Passes(%)"] = computeTeamstats_on_games["Passes(%)"].fillna(0)
    computeTeamstats_on_games["Crosses(%)"] = (
                100 * computeTeamstats_on_games["Accurate Crosses"] / computeTeamstats_on_games[
            "Total Crosses"]).round(1)
    computeTeamstats_on_games["Crosses(%)"] = computeTeamstats_on_games["Crosses(%)"].fillna(0)
    computeTeamstats_on_games["Long balls(%)"] = (
                100 * computeTeamstats_on_games["Accurate Long balls"] / computeTeamstats_on_games[
            "Total Long balls"]).round(1)
    computeTeamstats_on_games["Long balls(%)"] = computeTeamstats_on_games["Long balls(%)"].fillna(0)
    computeTeamstats_on_games["Duels(%)"] = (
                100 * computeTeamstats_on_games["Duels won"] / computeTeamstats_on_games["Duels"]).round(1)
    computeTeamstats_on_games["Duels(%)"] = computeTeamstats_on_games["Duels(%)"].fillna(0)
    computeTeamstats_on_games["Aerial duels(%)"] = (
                100 * computeTeamstats_on_games["Aerial duels won"] / computeTeamstats_on_games[
            "Aerial duels"]).round(1)
    computeTeamstats_on_games["Aerial duels(%)"] = computeTeamstats_on_games["Aerial duels(%)"].fillna(0)
    computeTeamstats_on_games["Ground duels(%)"] = (
                100 * computeTeamstats_on_games["Ground duels won"] / computeTeamstats_on_games[
            "Ground duels"]).round(1)
    computeTeamstats_on_games["Ground duels(%)"] = computeTeamstats_on_games["Ground duels(%)"].fillna(0)
    computeTeamstats_on_games["Runs out(%)"] = (
                100 * computeTeamstats_on_games["Runs out succ"] / computeTeamstats_on_games["Runs out"]).round(
        1)
    computeTeamstats_on_games["Runs out(%)"] = computeTeamstats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = dataset_filter.groupby(['idseason', 'Against'])[[
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
    computeAgainststats_on_games["Dribble(%)"] = (
                100 * computeAgainststats_on_games["Dribble attempts succ"] / computeAgainststats_on_games[
            "Dribble attempts"]).round(1)
    computeAgainststats_on_games["Dribble(%)"] = computeAgainststats_on_games["Dribble(%)"].fillna(0)
    computeAgainststats_on_games["Passes(%)"] = (
                100 * computeAgainststats_on_games["Accurate passes"] / computeAgainststats_on_games[
            "Total passes"]).round(1)
    computeAgainststats_on_games["Passes(%)"] = computeAgainststats_on_games["Passes(%)"].fillna(0)
    computeAgainststats_on_games["Crosses(%)"] = (
                100 * computeAgainststats_on_games["Accurate Crosses"] / computeAgainststats_on_games[
            "Total Crosses"]).round(1)
    computeAgainststats_on_games["Crosses(%)"] = computeAgainststats_on_games["Crosses(%)"].fillna(0)
    computeAgainststats_on_games["Long balls(%)"] = (
                100 * computeAgainststats_on_games["Accurate Long balls"] / computeAgainststats_on_games[
            "Total Long balls"]).round(1)
    computeAgainststats_on_games["Long balls(%)"] = computeAgainststats_on_games["Long balls(%)"].fillna(0)
    computeAgainststats_on_games["Duels(%)"] = (
                100 * computeAgainststats_on_games["Duels won"] / computeAgainststats_on_games["Duels"]).round(
        1)
    computeAgainststats_on_games["Duels(%)"] = computeAgainststats_on_games["Duels(%)"].fillna(0)
    computeAgainststats_on_games["Aerial duels(%)"] = (
                100 * computeAgainststats_on_games["Aerial duels won"] / computeAgainststats_on_games[
            "Aerial duels"]).round(1)
    computeAgainststats_on_games["Aerial duels(%)"] = computeAgainststats_on_games["Aerial duels(%)"].fillna(0)
    computeAgainststats_on_games["Ground duels(%)"] = (
                100 * computeAgainststats_on_games["Ground duels won"] / computeAgainststats_on_games[
            "Ground duels"]).round(1)
    computeAgainststats_on_games["Ground duels(%)"] = computeAgainststats_on_games["Ground duels(%)"].fillna(0)
    computeAgainststats_on_games["Runs out(%)"] = (
                100 * computeAgainststats_on_games["Runs out succ"] / computeAgainststats_on_games[
            "Runs out"]).round(1)
    computeAgainststats_on_games["Runs out(%)"] = computeAgainststats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = computeAgainststats_on_games.add_prefix('opp ').rename(
        columns={'opp Against': 'Team', 'opp idseason': 'idseason'})

    computeteamstats_on_games_total = pd.merge(computeTeamstats_on_games, computeAgainststats_on_games,
                                               on=['Team', 'idseason'])
    computeteamstats_on_games_total_sel = computeteamstats_on_games_total.loc[
        computeteamstats_on_games_total.Team == selected_Team]
    finaldataset = computeteamstats_on_games_total_sel[
        ['Against', 'Season', 'Phase', 'Round', 'Fixture', 'Home_Away', 'Result', "Goals", "opp Goals",
         'Assists', 'opp Assists', 'Yellow card', 'opp Yellow card', 'Red card',
         'opp Red card', 'Shots on target', 'opp Shots on target', 'Shots off target', 'opp Shots off target',
         'Shots blocked', 'opp Shots blocked', 'Dribble attempts succ', 'opp Dribble attempts succ',
         'Dribble attempts', 'opp Dribble attempts', "Dribble(%)", "opp Dribble(%)", 'Penalty won',
         'Big chances missed', 'opp Big chances missed', 'Penalty miss', 'opp Penalty miss',
         'Hit woodwork', 'opp Hit woodwork', 'Offsides', 'opp Offsides', 'Defensive actions',
         'opp Defensive actions', 'Clearances', 'opp Clearances',
         'Interceptions', 'opp Interceptions', 'Total tackles', 'opp Total tackles', 'Dribbled past',
         'Penalty committed', 'Own goals', 'opp Own goals', 'Last man tackle', 'opp Last man tackle',
         'Error led to shot', 'opp Error led to shot', 'Clearance off line', 'opp Clearance off line',
         'Error led to goal', 'opp Error led to goal', 'Duels won', "Duels(%)",
         'opp Duels won', "opp Duels(%)", 'Ground duels', 'Ground duels won', "Ground duels(%)",
         'opp Ground duels won', "opp Ground duels(%)",
         'Aerial duels', 'Aerial duels won', "Aerial duels(%)", 'opp Aerial duels won', "opp Aerial duels(%)",
         'Possession lost', 'opp Possession lost',
         'Fouls', 'opp Fouls', 'Touches', 'opp Touches', 'Accurate passes', 'Total passes', "Passes(%)",
         'opp Accurate passes', 'opp Total passes', "opp Passes(%)", 'Key passes', 'opp Key passes',
         'Total Crosses', 'Accurate Crosses', "Crosses(%)", 'opp Total Crosses', 'opp Accurate Crosses',
         "opp Crosses(%)", 'Total Long balls', 'Accurate Long balls', "Long balls(%)",
         'opp Total Long balls', 'opp Accurate Long balls', "opp Long balls(%)", 'Big chances created',
         'opp Big chances created', 'Saves', 'opp Saves',
         'Punches', 'opp Punches', 'Runs out', 'Runs out succ', "Runs out(%)", 'opp Runs out',
         'opp Runs out succ', "opp Runs out(%)",
         'High claims', 'opp High claims', 'Saves from inside box', 'opp Saves from inside box',
         'Penalties saved', 'opp Penalties saved']].rename(
        columns={'Accurate passes': 'Accurate Passes', 'Total passes': 'Total Passes',
                 'Key passes': 'Key Passes', 'opp Accurate passes': 'opp Accurate Passes',
                 'opp Total passes': 'opp Total Passes', 'opp Key passes': 'opp Key Passes',
                 'Penalties saved': 'Penalty saved', 'opp Penalties saved': 'opp Penalty saved',
                 'Clearance off line': 'Clearances off line',
                 'opp Clearance off line': 'opp Clearances off line'})
    statselectors = st.selectbox("Select Stat:",
                                 ["All", 'Goals', 'Assists', 'Yellow card', 'Red card', 'Shots', 'Dribble',
                                  'Penalty', 'Big chances', 'Hit woodwork', 'Offsides',
                                  'Defensive actions', 'Clearances', 'Interceptions', 'Total tackles',
                                  'Own goals', 'Last man tackle', 'Error led to shot', 'Error led to goal',
                                  'Duels', 'Ground duels', 'Aerial duels',
                                  'Possession lost', 'Foul', 'Touches', 'Passes', 'Crosses', 'Long balls',
                                  'Saves', 'Punches', 'Runs out', 'High claims'])
    if statselectors == "All":

        interactive_table(finaldataset.set_index('Against').sort_values('Fixture'),
                          paging=False, height=900, width=2000, showIndex=True,
                          classes="display order-column nowrap table_with_monospace_font", searching=True,
                          fixedColumns=True, select=True, info=False, scrollCollapse=True,
                          scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                          columnDefs=[{"className": "dt-center", "targets": "_all"}])
    else:
        regex1 = "Against|Season|Phase|Round|Fixture|Home_Away|Result|" + statselectors

        interactive_table(finaldataset.filter(regex=regex1).set_index('Against').sort_values('Fixture'),
                          paging=False, height=900, width=2000, showIndex=True,
                          classes="display order-column nowrap table_with_monospace_font", searching=True,
                          fixedColumns=True, select=True, info=False, scrollCollapse=True,
                          scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                          columnDefs=[{"className": "dt-center", "targets": "_all"}])


except:
    st.error('No data available for these parameters')
