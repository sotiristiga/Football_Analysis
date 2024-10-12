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

selected_Player1 = st.sidebar.selectbox("Choose First Player:", dataset['Player'].reset_index().sort_values('Player')['Player'].unique())
selected_ha1 = st.sidebar.selectbox("Home or Away games (First Player):",['Away', 'Home', 'All'],index=2)
selected_season1 = st.sidebar.selectbox("Season (First Player):",['All','2024-2025'],index=0)
selected_phase1 = st.sidebar.selectbox("Phase (First Player):",['Regular Season', 'Play offs', 'Play out','All'],index=3)
selected_wl1 = st.sidebar.selectbox("Result (First Player):",['Win','Draw', 'Lose','All'],index=3)
selected_round1 = st.sidebar.selectbox("Round (First Player):",['First Round', 'Second Round', 'All'],index=2)

st.sidebar.write("## ")
st.sidebar.write("## Second Player filters")
selected_Player2 = st.sidebar.selectbox("Choose Second Player:", dataset['Player'].reset_index().sort_values('Player')['Player'].unique(),index=1)
selected_ha2 = st.sidebar.selectbox("Home or Away games (Second Player):",['Away', 'Home', 'All'],index=2)
selected_season2 = st.sidebar.selectbox("Season (Second Player):",['All','2024-2025'],index=0)
selected_phase2 = st.sidebar.selectbox("Phase (Second Player):",['Regular Season', 'Play offs', 'Play out','All'],index=3)
selected_wl2 = st.sidebar.selectbox("Result (Second Player):",['Win','Draw', 'Lose','All'],index=3)
selected_round2 = st.sidebar.selectbox("Round (Second Player):",['First Round', 'Second Round', 'All'],index=2)

try:

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






    if "All" in selected_ha2:
        selected_ha2 = ['Away', 'Home',]
        dataset_filter2=dataset.loc[dataset['Home_Away'].isin(selected_ha2)]
        select_ha2=''
    else:
        dataset_filter2=dataset.loc[dataset['Home_Away']==selected_ha2]
        select_ha2 = selected_ha2

    if "All" in selected_season2:
        selected_season2 = ['2016-2017', '2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022', '2022-2023','2023-2024','2024-2025']
        dataset_filter2=dataset_filter2.loc[dataset_filter2['Season'].isin(selected_season2)]
        select_season2 = ''
    else:
        dataset_filter2=dataset_filter2.loc[dataset_filter2['Season']==selected_season2]
        select_season2 = selected_season2


    if "All" in selected_wl2:
        selected_wl2 = ['Win','Draw', 'Lose']
        dataset_filter2 = dataset_filter2.loc[dataset_filter2['Result'].isin(selected_wl2)]
        select_wl2 = ''
    else:
        dataset_filter2= dataset_filter2.loc[dataset_filter2['Result'] == selected_wl2]
        select_wl2 = selected_wl2

    if "All" in selected_phase2:
        selected_phase2 = ['Regular Season', 'Play offs', 'Play out']
        dataset_filter2 = dataset_filter2.loc[dataset_filter2['Phase'].isin(selected_phase2)]
        select_phase2 = ''
    else:
        dataset_filter2 = dataset_filter2.loc[dataset_filter2['Phase'] == selected_phase2]
        select_phase2 = selected_phase2

    if "All" in selected_round2:
        selected_round2 = ['First Round', 'Second Round' ]
        dataset_filter2 = dataset_filter2.loc[dataset_filter2['Round'].isin(selected_round2)]
        select_round2 = ''
    else:
        dataset_filter2 = dataset_filter2.loc[dataset_filter2['Round'] == selected_round2]
        select_round2 = selected_round2




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

    def computeplayerstats(data,player,sls,slp,slr,slha,slwl):
        games = data['Player'].value_counts().reset_index().rename(columns={'count': 'Games'})
        computeplayerstats_total = data.groupby('Player')[['Minutes played',
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
        computeplayerstats_total_sel=computeplayerstats_total.loc[computeplayerstats_total.Player==player]

        computeplayerstats_mean = data.groupby('Player')[['Minutes played',
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
                    'Was fouled', 'Saves', 'Punches', 'Runs out succ', 'Runs out', "Runs out(%)", 'High claims',
                    'Saves from inside box', 'Penalties saved', 'Defensive actions']
        colsminus = ['Red card', 'Big chances missed', 'Penalty miss', 'Hit woodwork', 'Dribbled past', 'Penalty committed',
                     'Own goals', 'Error led to shot', 'Error led to goal', 'Possession lost',
                     'Fouls', 'Offsides']
        players_ratings1 = player_rating_stat_higher(computeplayerstats_mean, 'Goals')
        for i in colsplus:
            df2 = player_rating_stat_higher(computeplayerstats_mean, i)
            players_ratings1 = pd.merge(players_ratings1, df2)

        players_ratings2 = player_rating_stat_lower(computeplayerstats_mean, 'Yellow card')
        for i in colsminus:
            df3 = player_rating_stat_lower(computeplayerstats_mean, i)
            players_ratings2 = pd.merge(players_ratings2, df3)

        players_ratings = pd.merge(players_ratings1, players_ratings2)
        computeplayerstats_mean_sel=computeplayerstats_mean.loc[computeplayerstats_mean.Player==player]
        computeplayerstats_mean_sel['Player']=computeplayerstats_mean_sel['Player']+" "+sls+" "+slp+" "+slr+" "+slha+" "+slwl
        computeplayerstats_total_sel['Player'] = computeplayerstats_total_sel['Player'] + " " + sls + " " + slp + " " + slr + " " + slha + " " + slwl
        players_ratings_sel=players_ratings.loc[players_ratings.Player==player]
        computeplayerstats_total_sel['Player'] = computeplayerstats_total_sel[
                                                     'Player'] + " " + sls + " " + slp + " " + slr + " " + slha + " " + slwl
        return [computeplayerstats_total_sel,computeplayerstats_mean_sel,players_ratings_sel]


    finaltotal=pd.concat([computeplayerstats(dataset_filter1,selected_Player1,select_season1,select_phase1,select_round1,select_ha1,select_wl1)[0],
                          computeplayerstats(dataset_filter2,selected_Player2,select_season2,select_phase2,select_round2,select_ha2,select_wl2)[0]])

    finalmean=pd.concat([computeplayerstats(dataset_filter1,selected_Player1,select_season1,select_phase1,select_round1,select_ha1,select_wl1)[1],
                          computeplayerstats(dataset_filter2,selected_Player2,select_season2,select_phase2,select_round2,select_ha2,select_wl2)[1]])
    player1_ratings=computeplayerstats(dataset_filter1,selected_Player1,select_season1,select_phase1,select_round1,select_ha1,select_wl1)[2]
    player2_ratings=computeplayerstats(dataset_filter2,selected_Player2,select_season2,select_phase2,select_round2,select_ha2,select_wl2)[2]

    player1,player2=st.columns(2)
    with player1:
        st.write('##### Player 1: '+ selected_Player1)
        st.write('##### Team: '+dataset_filter1.loc[dataset_filter1.Player==selected_Player1]['Team'].unique()[0])
        st.write('##### Position: ' + dataset_filter1.loc[dataset_filter1.Player == selected_Player1]['Position'].unique()[0])
        st.write("Season: "+select_season1)
        st.write('Phase: '+select_phase1)
        st.write('Round: '+select_round1)
        st.write('Home or Away: '+select_ha1)
        st.write('Result: '+select_wl1)
        ov1=go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=player1_ratings.melt(id_vars='Player')['value'].mean().round(0),
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={'axis': {'range': [None, 100]},
                               'bordercolor': "gray"},
                        title={'text': "Overall<br>Rating<br>"+ selected_Player1}))

        ov1.update_layout(
                    autosize=False,
                    width=200,
                    height=250,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(ov1)
    with player2:
        st.write('##### Player 2: '+ selected_Player2)
        st.write('##### Team: '+dataset_filter2.loc[dataset_filter2.Player==selected_Player2]['Team'].unique()[0])
        st.write('##### Position: ' + dataset_filter2.loc[dataset_filter2.Player == selected_Player2]['Position'].unique()[0])
        st.write("Season: "+select_season2)
        st.write('Phase: '+select_phase2)
        st.write('Round: '+select_round2)
        st.write('Home or Away: '+select_ha2)
        st.write('Result: '+select_wl2)
        ov2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=player2_ratings.melt(id_vars='Player')['value'].mean().round(0),
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [None, 100]},
                   'bordercolor': "gray"},
            title={'text': "Overall<br>Rating<br>"+ selected_Player2}))

        ov2.update_layout(
            autosize=False,
            width=200,
            height=250,
            margin=dict(
                l=30,
                r=50,
                b=0,
                t=0,
                pad=0
            ))

        st.write(ov2)
    st.write("#### Basic Stats")
    totalbasic,pergamebasic=st.tabs(['Total','Per Game'])
    with totalbasic:
        basic_stats_total=finaltotal[['Player','Games','Minutes played','Goals', 'Assists', 'Yellow card', 'Red card']]

        interactive_table(
            basic_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    with pergamebasic:
        basic_stats_mean=finalmean[['Player','Games','Minutes played','Goals', 'Assists', 'Yellow card', 'Red card']]
        interactive_table(
            basic_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])



    st.write("#### Attack Stats")
    totalattack, pergameattack = st.tabs(['Total', 'Per Game'])
    with totalattack:
        attack_stats_total = finaltotal[
            ['Player', 'Shots on target', 'Shots off target', 'Shots blocked', 'Dribble attempts succ',
             'Dribble attempts', "Dribble(%)", 'Penalty won', 'Big chances missed', 'Penalty miss',
             'Hit woodwork', 'Offsides']]
        interactive_table(
            attack_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    with pergameattack:
        attack_stats_mean = finalmean[
            ['Player', 'Shots on target', 'Shots off target', 'Shots blocked', 'Dribble attempts succ',
             'Dribble attempts', "Dribble(%)", 'Penalty won', 'Big chances missed', 'Penalty miss',
             'Hit woodwork', 'Offsides']]
        interactive_table(
            attack_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    attack1=player1_ratings[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',
             'Rating Dribble attempts', "Rating Dribble(%)", 'Rating Penalty won', 'Rating Big chances missed', 'Rating Penalty miss',
             'Rating Hit woodwork', 'Rating Offsides','Rating Goals']]
    attack2=player2_ratings[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',
             'Rating Dribble attempts', "Rating Dribble(%)", 'Rating Penalty won', 'Rating Big chances missed', 'Rating Penalty miss',
             'Rating Hit woodwork', 'Rating Offsides','Rating Goals']]
    attack1sel=(attack1[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',"Rating Dribble(%)",'Rating Big chances missed']]
                .rename(columns={'Rating Shots on target':'Shots<br>on<br>target', 'Rating Shots off target':'Shots<br>off<br>target', 'Rating Shots blocked':'Shots<br>blocked',
                                 'Rating Dribble attempts succ':'Dribble<br>attempts<br>succ',"Rating Dribble(%)":"Dribble(%)",'Rating Big chances missed':'Big<br>chances<br>missed'
                                 })
                .melt())
    attack1sel['variable']=attack1sel['variable'].replace('Rating ','')
    attack2sel=(attack2[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',"Rating Dribble(%)",'Rating Big chances missed']]
                .rename(columns={'Rating Shots on target':'Shots<br>on<br>target', 'Rating Shots off target':'Shots<br>off<br>target', 'Rating Shots blocked':'Shots<br>blocked',
                                 'Rating Dribble attempts succ':'Dribble<br>attempts<br>succ',"Rating Dribble(%)":"Dribble(%)",'Rating Big chances missed':'Big<br>chances<br>missed'})
                .melt())
    attack2sel['variable']=attack2sel['variable'].replace('Rating ','')
    gauge1att,starattack,gauge2att=st.columns([1,2,1])
    with gauge1att:
        gauge1attack=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=attack1.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Attack<br>Rating<br>"+selected_Player1}))

        gauge1attack.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge1attack)
    with starattack:
        staratt = go.Figure()
        staratt.add_trace(go.Scatterpolar(r=attack1sel['value'],theta=attack1sel['variable'],
          fill='toself',name=selected_Player1 + " "+select_season1+" "+select_phase1+" "+select_round1+" "+select_ha1+" "+select_wl1,line_color = 'peru',
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))
        staratt.add_trace(go.Scatterpolar(r=attack2sel['value'], theta=attack2sel['variable'], fill='toself',
                                          name=selected_Player2 + " " + select_season2 + " " + select_phase2 + " " + select_round2 + " " + select_ha2 + " " + select_wl2,
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

        staratt.update_layout(
            width=550,
            height=400,
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ))
        )
        st.write(staratt)
    with gauge2att:
        gauge2attack=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=attack2.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Attack<br>Rating<br>"+selected_Player2}))

        gauge2attack.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge2attack)


    st.write("#### Defence Stats")
    totaldefence, pergamedefence = st.tabs(['Total', 'Per Game'])
    with totaldefence:
        defence_stats_total = finaltotal[
            ['Player', 'Defensive actions', 'Clearances', 'Blocked shots', 'Interceptions', 'Total tackles',
             'Dribbled past',
             'Penalty committed', 'Own goals', 'Last man tackle', 'Error led to shot', 'Clearance off line',
             'Error led to goal']]
        interactive_table(
            defence_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])
    with pergamedefence:
        defence_stats_mean = finalmean[
            ['Player', 'Defensive actions', 'Clearances', 'Blocked shots', 'Interceptions', 'Total tackles',
             'Dribbled past',
             'Penalty committed', 'Own goals', 'Last man tackle', 'Error led to shot', 'Clearance off line',
             'Error led to goal']]
        interactive_table(
            defence_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])


    defence1=player1_ratings[['Rating Defensive actions', 'Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
             'Rating Dribbled past',
             'Rating Penalty committed', 'Rating Own goals', 'Rating Last man tackle', 'Rating Error led to shot', 'Rating Clearance off line',
             'Rating Error led to goal']]
    defence2=player2_ratings[['Rating Defensive actions', 'Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
             'Rating Dribbled past',
             'Rating Penalty committed', 'Rating Own goals', 'Rating Last man tackle', 'Rating Error led to shot', 'Rating Clearance off line',
             'Rating Error led to goal']]
    defence1sel=(defence1[['Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
             'Rating Dribbled past']]
                .rename(columns={'Rating Clearances':'Clearances', 'Rating Blocked shots':'Blocked<br>shots', 'Rating Interceptions':'Interceptions',
                                 'Rating Total tackles':'Total<br>tackles',"Rating Dribbled past":"Dribbled<br>past"})
                .melt())
    defence1sel['variable']=defence1sel['variable'].replace('Rating ','')
    defence2sel=(defence2[['Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
             'Rating Dribbled past']]
                .rename(columns={'Rating Clearances':'Clearances', 'Rating Blocked shots':'Blocked<br>shots', 'Rating Interceptions':'Interceptions',
                                 'Rating Total tackles':'Total<br>tackles',"Rating Dribbled past":"Dribbled<br>past"})
                .melt())
    defence2sel['variable']=defence2sel['variable'].replace('Rating ','')
    gauge1def,stardef,gauge2def=st.columns([1,2,1])
    with gauge1def:
        gauge1defence=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=defence1.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Defence<br>Rating<br>"+selected_Player1}))

        gauge1defence.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge1defence)
    with stardef:
        stardef = go.Figure()
        stardef.add_trace(go.Scatterpolar(r=defence1sel['value'],theta=defence1sel['variable'],
          fill='toself',name=selected_Player1 + " "+select_season1+" "+select_phase1+" "+select_round1+" "+select_ha1+" "+select_wl1,line_color = 'peru',
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))
        stardef.add_trace(go.Scatterpolar(r=defence2sel['value'], theta=defence2sel['variable'], fill='toself',
                                          name=selected_Player2 + " " + select_season2 + " " + select_phase2 + " " + select_round2 + " " + select_ha2 + " " + select_wl2,
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

        stardef.update_layout(
            width=550,
            height=400,
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ))
        )
        st.write(stardef)
    with gauge2def:
        gauge2defence=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=defence2.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Defence<br>Rating<br>"+selected_Player2}))

        gauge2defence.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge2defence)

    st.write("#### Duels Stats")
    totalduels, pergameduels = st.tabs(['Total', 'Per Game'])
    with totalduels:
        duels_stats_total = finaltotal[
            ['Player', 'Duels', 'Duels won',"Duels(%)", 'Ground duels', 'Ground duels won','Ground duels(%)', 'Aerial duels', 'Aerial duels won','Aerial duels(%)',
             'Possession lost', 'Fouls', 'Was fouled']]
        interactive_table(
            duels_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    with pergameduels:
        duels_stats_mean = finalmean[
            ['Player', 'Duels', 'Duels won',"Duels(%)", 'Ground duels', 'Ground duels won','Ground duels(%)', 'Aerial duels', 'Aerial duels won','Aerial duels(%)',
             'Possession lost', 'Fouls', 'Was fouled']]
        interactive_table(
            duels_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])


    duels1=player1_ratings[['Rating Duels', 'Rating Duels won',"Rating Duels(%)", 'Rating Ground duels', 'Rating Ground duels won','Rating Ground duels(%)', 'Rating Aerial duels',
                            'Rating Aerial duels won','Rating Aerial duels(%)','Rating Possession lost', 'Rating Fouls', 'Rating Was fouled']]
    duels2=player2_ratings[['Rating Duels', 'Rating Duels won',"Rating Duels(%)", 'Rating Ground duels', 'Rating Ground duels won','Rating Ground duels(%)', 'Rating Aerial duels',
                            'Rating Aerial duels won','Rating Aerial duels(%)','Rating Possession lost', 'Rating Fouls', 'Rating Was fouled']]
    duels1sel=(duels1[['Rating Duels won',"Rating Duels(%)", 'Rating Ground duels won','Rating Ground duels(%)','Rating Aerial duels won','Rating Aerial duels(%)',
             'Rating Possession lost']]
                .rename(columns={'Rating Duels won':'Duels<br>won', 'Rating Duels(%)':'Duels(%)', 'Rating Ground duels won':'Ground<br>duels<br>won',
                                 'Rating Ground duels(%)':'Ground<br>duels(%)',"Rating Aerial duels won":"Aerial<br>duels<br>won",'Rating Aerial duels(%)':'Aerial<br>duels(%)',
                                 'Rating Possession lost':'Possession<br>lost'})
                .melt())
    duels1sel['variable']=duels1sel['variable'].replace('Rating ','')
    duels2sel=(duels2[['Rating Duels won',"Rating Duels(%)", 'Rating Ground duels won','Rating Ground duels(%)','Rating Aerial duels won','Rating Aerial duels(%)',
             'Rating Possession lost']]
                .rename(columns={'Rating Duels won':'Duels<br>won', 'Rating Duels(%)':'Duels(%)', 'Rating Ground duels won':'Ground<br>duels<br>won',
                                 'Rating Ground duels(%)':'Ground<br>duels(%)',"Rating Aerial duels won":"Aerial<br>duels<br>won",'Rating Aerial duels(%)':'Aerial<br>duels(%)',
                                 'Rating Possession lost':'Possession<br>lost'})
                .melt())
    duels2sel['variable']=duels2sel['variable'].replace('Rating ','')
    gauge1due,stardue,gauge2due=st.columns([1,2,1])
    with gauge1due:
        gauge1duels=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=duels1.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Duels<br>Rating<br>"+selected_Player1}))

        gauge1duels.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge1duels)
    with stardue:
        stardue = go.Figure()
        stardue.add_trace(go.Scatterpolar(r=duels1sel['value'],theta=duels1sel['variable'],
          fill='toself',name=selected_Player1 + " "+select_season1+" "+select_phase1+" "+select_round1+" "+select_ha1+" "+select_wl1,line_color = 'peru',
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))
        stardue.add_trace(go.Scatterpolar(r=duels2sel['value'], theta=duels2sel['variable'], fill='toself',
                                          name=selected_Player2 + " " + select_season2 + " " + select_phase2 + " " + select_round2 + " " + select_ha2 + " " + select_wl2,
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

        stardue.update_layout(
            width=550,
            height=400,
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ))
        )
        st.write(stardue)

    with gauge2due:
        gauge2duels=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=duels2.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Duels<br>Rating<br>"+selected_Player2}))

        gauge2duels.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge2duels)

    st.write("#### Passing Stats")
    totalpass, pergamepass = st.tabs(['Total', 'Per Game'])
    with totalpass:
        passing_stats_total = finaltotal[
            ['Player', 'Touches', 'Accurate passes', 'Total passes', "Passes(%)", 'Key passes', 'Accurate Crosses',
             'Total Crosses', "Crosses(%)", 'Accurate Long balls', 'Total Long balls', "Long balls(%)",
             'Big chances created']]
        interactive_table(
            passing_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    with pergamepass:
        passing_stats_mean = finalmean[
            ['Player', 'Touches', 'Accurate passes', 'Total passes', "Passes(%)", 'Key passes', 'Accurate Crosses',
             'Total Crosses', "Crosses(%)", 'Accurate Long balls', 'Total Long balls', "Long balls(%)",
             'Big chances created']]
        interactive_table(
            passing_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])


    pass1=player1_ratings[['Rating Touches', 'Rating Accurate passes', 'Rating Total passes', "Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses',
             'Rating Total Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls', 'Rating Total Long balls', "Rating Long balls(%)",
             'Rating Big chances created','Rating Assists']]
    pass2=player2_ratings[['Rating Touches', 'Rating Accurate passes', 'Rating Total passes', "Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses',
             'Rating Total Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls', 'Rating Total Long balls', "Rating Long balls(%)",
             'Rating Big chances created','Rating Assists']]
    pass1sel=(pass1[['Rating Touches', 'Rating Accurate passes',"Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls',
                     "Rating Long balls(%)",'Rating Big chances created']]
                .rename(columns={'Rating Touches':'Touches', 'Rating Accurate passes':'Accurate<br>passes', 'Rating Passes(%)':'Passes(%)',
                                 'Rating Key passes':'Key<br>passes','Rating Accurate Crosses':"Accurate<br>Crosses",'Rating Crosses(%)':'Crosses(%)',
                                 'Rating Accurate Long balls':'Accurate<br>Long<br>balls',"Rating Long balls(%)":"Long<br>balls(%)",'Rating Big chances created':'Big<br>chances<br>created'})
                .melt())
    pass1sel['variable']=pass1sel['variable'].replace('Rating ','')
    pass2sel=(pass2[['Rating Touches', 'Rating Accurate passes',"Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls',
                     "Rating Long balls(%)",'Rating Big chances created']]
                .rename(columns={'Rating Touches':'Touches', 'Rating Accurate passes':'Accurate<br>passes', 'Rating Passes(%)':'Passes(%)',
                                 'Rating Key passes':'Key<br>passes','Rating Accurate Crosses':"Accurate<br>Crosses",'Rating Crosses(%)':'Crosses(%)',
                                 'Rating Accurate Long balls':'Accurate<br>Long<br>balls',"Rating Long balls(%)":"Long<br>balls(%)",'Rating Big chances created':'Big<br>chances<br>created'})
                .melt())
    pass2sel['variable']=pass2sel['variable'].replace('Rating ','')
    gauge1pass,starpass,gauge2pass=st.columns([1,2,1])
    with gauge1pass:
        gauge1pass=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pass1.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Passing<br>Rating<br>"+selected_Player1}))

        gauge1pass.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge1pass)
    with starpass:
        starpass = go.Figure()
        starpass.add_trace(go.Scatterpolar(r=pass1sel['value'],theta=pass1sel['variable'],
          fill='toself',name=selected_Player1 + " "+select_season1+" "+select_phase1+" "+select_round1+" "+select_ha1+" "+select_wl1,line_color = 'peru',
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))
        starpass.add_trace(go.Scatterpolar(r=pass2sel['value'], theta=pass2sel['variable'], fill='toself',
                                          name=selected_Player2 + " " + select_season2 + " " + select_phase2 + " " + select_round2 + " " + select_ha2 + " " + select_wl2,
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

        starpass.update_layout(
            width=550,
            height=400,
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ))
        )
        st.write(starpass)

    with gauge2pass:
        gauge2pass=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pass2.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Passing<br>Rating<br>"+selected_Player2}))

        gauge2pass.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge2pass)


    st.write("#### Goalkeeping Stats")
    totalgk, pergamegk = st.tabs(['Total', 'Per Game'])
    with totalgk:
        goalkeeping_stats_total = finaltotal[
            ['Player', 'Saves', 'Punches', 'Runs out succ', 'Runs out', 'Runs out(%)','High claims', 'Saves from inside box',
             'Penalties saved']]
        interactive_table(
            goalkeeping_stats_total.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])
    with pergamegk:
        goalkeeping_stats_mean = finalmean[
            ['Player', 'Saves', 'Punches', 'Runs out succ', 'Runs out', 'Runs out(%)', 'High claims', 'Saves from inside box',
             'Penalties saved']]
        interactive_table(
            goalkeeping_stats_mean.set_index('Player'),
            paging=False, height=900, width=2000, showIndex=True,
            classes="display order-column nowrap table_with_monospace_font", searching=True,
            fixedColumns=True, select=True, info=False, scrollCollapse=True,
            scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
            columnDefs=[{"className": "dt-center", "targets": "_all"}])

    gk1=player1_ratings[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box',
             'Rating Penalties saved']]
    gk2=player2_ratings[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box',
             'Rating Penalties saved']]
    gk1sel=(gk1[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box']]
                .rename(columns={'Rating Saves':'Saves', 'Rating Punches':'Punches', 'Rating Runs out succ':'Runs<br>out<br>succ',
                                 'Rating Runs out(%)':'Runs<br>out(%)','Rating High claims':"High<br>claims",'Rating Saves from inside box':'Saves<br>from<br>inside<br>box'})
                .melt())
    gk1sel['variable']=gk1sel['variable'].replace('Rating ','')
    gk2sel=(gk2[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box']]
                .rename(columns={'Rating Saves':'Saves', 'Rating Punches':'Punches', 'Rating Runs out succ':'Runs<br>out<br>succ',
                                 'Rating Runs out(%)':'Runs<br>out(%)','Rating High claims':"High<br>claims",'Rating Saves from inside box':'Saves<br>from<br>inside<br>box'})
                .melt())
    gk2sel['variable']=gk2sel['variable'].replace('Rating ','')
    gauge1gk,stargk,gauge2gk=st.columns([1,2,1])
    with gauge1gk:
        gauge1gk=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=gk1.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Goalkeeping<br>Rating<br>"+selected_Player1}))

        gauge1gk.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge1gk)
    with stargk:
        stargk = go.Figure()
        stargk.add_trace(go.Scatterpolar(r=gk1sel['value'],theta=gk1sel['variable'],
          fill='toself',name=selected_Player1 + " "+select_season1+" "+select_phase1+" "+select_round1+" "+select_ha1+" "+select_wl1,line_color = 'peru',
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))
        stargk.add_trace(go.Scatterpolar(r=gk2sel['value'], theta=gk2sel['variable'], fill='toself',
                                          name=selected_Player2 + " " + select_season2 + " " + select_phase2 + " " + select_round2 + " " + select_ha2 + " " + select_wl2,
                                          hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

        stargk.update_layout(
            width=550,
            height=400,
            showlegend=True,
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ))
        )
        st.write(stargk)

    with gauge2gk:
        gauge2gk=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=gk2.melt()['value'].mean().round(0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 100]},
                           'bordercolor': "gray"},
                    title={'text': "Goalkeeping<br>Rating<br>"+selected_Player2}))

        gauge2gk.update_layout(
                    autosize=False,
                    width=250,
                    height=300,
                    margin=dict(
                        l=30,
                        r=50,
                        b=0,
                        t=0,
                        pad=0
                    ))

        st.write(gauge2gk)
except:
    st.error('No data availale with these parameters')
