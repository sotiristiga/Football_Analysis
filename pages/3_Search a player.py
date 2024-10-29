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



st.set_page_config(layout='wide', page_title="Search a Player")

dataset2324=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2324.csv")
dataset2425=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")
dataset=pd.concat([dataset2324,dataset2425])

selected_ha = st.sidebar.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
selected_season = st.sidebar.selectbox("Season:",['All',"2023-2024",'2024-2025'],index=2)
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
    selected_season = ['2016-2017', '2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022', '2022-2023','2023-2024','2024-2025']
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
                'Was fouled', 'Saves', 'Punches', 'Runs out succ', 'Runs out', "Runs out(%)", 'High claims',
                'Saves from inside box', 'Penalties saved', 'Defensive actions']
colsminus = ['Red card', 'Big chances missed', 'Penalty miss', 'Hit woodwork', 'Dribbled past', 'Penalty committed',
             'Own goals', 'Error led to shot', 'Error led to goal', 'Possession lost',
             'Fouls', 'Offsides']

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
Superstats,bygame=st.tabs(['Superleague Stats','Stats by game'])
with Superstats:
    player,over=st.columns(2)
    with player:
        selected_Player = st.selectbox("Player:", dataset_filter['Player'].reset_index().sort_values('Player')['Player'].unique())
        computeplayerstats_total_sel=computeplayerstats_total.loc[computeplayerstats_total.Player==selected_Player]
        computeplayerstats_mean_sel=computeplayerstats_mean.loc[computeplayerstats_mean.Player==selected_Player]
        computeplayerstats_mean_sel['Player']=computeplayerstats_mean_sel['Player']+" "+select_season+" "+select_phase+" "+select_round+" "+select_ha+" "+select_wl
        computeplayerstats_total_sel['Player'] = computeplayerstats_total_sel['Player'] + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl
        players_ratings_sel = players_ratings.loc[players_ratings.Player == selected_Player]
        try:
            st.write('##### Team: '+dataset_filter.loc[dataset_filter.Player==selected_Player]['Team'].unique()[0])
            st.write('##### Position: ' + dataset_filter.loc[dataset_filter.Player == selected_Player]['Position'].unique()[0])
        except:
            st.error('No data available with these parameters')

    with over:
        try:
            ov=go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=players_ratings_sel.melt(id_vars='Player')['value'].mean().round(0),
                                domain={'x': [0, 1], 'y': [0, 1]},
                                gauge={'axis': {'range': [None, 100]},
                                       'bordercolor': "gray"},
                                title={'text': "Overall<br>Rating"}))

            ov.update_layout(
                        autosize=False,
                        width=150,
                        height=200,
                        margin=dict(
                            l=0,
                            r=0,
                            b=0,
                            t=20,
                            pad=0
                        ))

            st.write(ov)
        except:
            st.error('No data available with these parameters')

    try:
        st.write("#### Basic Stats")
        totalbasic,pergamebasic=st.tabs(['Total','Per Game'])
        with totalbasic:
            basic_stats_total=computeplayerstats_total_sel[['Player','Games','Minutes played','Goals', 'Assists', 'Yellow card', 'Red card']]

            interactive_table(
                basic_stats_total.set_index('Player'),
                paging=False, height=990, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])
        with pergamebasic:
            basic_stats_mean=computeplayerstats_mean_sel[['Player','Games','Minutes played','Goals', 'Assists', 'Yellow card', 'Red card']]
            interactive_table(
                basic_stats_mean.set_index('Player'),
                paging=False, height=990, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])


        st.write("#### Attack Stats")
        totalattack, pergameattack = st.tabs(['Total', 'Per Game'])
        with totalattack:
            attack_stats_total = computeplayerstats_total_sel[
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
            attack_stats_mean = computeplayerstats_mean_sel[
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


        attack=players_ratings_sel[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',
                 'Rating Dribble attempts', "Rating Dribble(%)", 'Rating Penalty won', 'Rating Big chances missed', 'Rating Penalty miss',
                 'Rating Hit woodwork', 'Rating Offsides','Rating Goals']]

        attacksel=(attack[['Rating Shots on target', 'Rating Shots off target', 'Rating Shots blocked', 'Rating Dribble attempts succ',"Rating Dribble(%)",'Rating Big chances missed']]
                    .rename(columns={'Rating Shots on target':'Shots<br>on<br>target', 'Rating Shots off target':'Shots<br>off<br>target', 'Rating Shots blocked':'Shots<br>blocked',
                                     'Rating Dribble attempts succ':'Dribble<br>attempts<br>succ',"Rating Dribble(%)":"Dribble(%)",'Rating Big chances missed':'Big<br>chances<br>missed'
                                     })
                    .melt())
        try:
            gaugeatt,starattack=st.columns([1,1])
            with gaugeatt:
                gaugeattack=go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=attack.melt()['value'].mean().round(0),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={'axis': {'range': [None, 100]},
                                   'bordercolor': "gray"},
                            title={'text': "Attack<br>Rating<br>"}))

                gaugeattack.update_layout(
                            autosize=False,
                            width=200,
                            height=200,
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=70,
                                pad=0
                            ))

                st.write(gaugeattack)
            with starattack:
                staratt = go.Figure()
                staratt.add_trace(go.Barpolar(r=attacksel['value'],theta=attacksel['variable'],
                  name=selected_Player + " "+select_season+" "+select_phase+" "+select_round+" "+select_ha+" "+select_wl,marker_color='peru',
                    marker_line_color="black",
                    marker_line_width=2,
                    opacity=0.8,hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))


                staratt.update_layout(
                    width=300,
                    height=300,
                    showlegend=False,
                margin = dict(
                    l=50,
                    r=40,
                    b=10,
                    t=10,
                    pad=0
                ),
                    polar=dict(
                        radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
                        angularaxis=dict(showticklabels=True, ticks='')
                    )
                )
                st.write(staratt)
        except:
            st.error('No data available with these parameters')
        st.write("#### Defence Stats")
        totaldefence, pergamedefence = st.tabs(['Total', 'Per Game'])
        with totaldefence:
            defence_stats_total = computeplayerstats_total_sel[
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
            defence_stats_mean = computeplayerstats_mean_sel[
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
        defence=players_ratings_sel[['Rating Defensive actions', 'Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
                 'Rating Dribbled past',
                 'Rating Penalty committed', 'Rating Own goals', 'Rating Last man tackle', 'Rating Error led to shot', 'Rating Clearance off line',
                 'Rating Error led to goal']]
        defencesel=(defence[['Rating Clearances', 'Rating Blocked shots', 'Rating Interceptions', 'Rating Total tackles',
                 'Rating Dribbled past']]
                    .rename(columns={'Rating Clearances':'Clearances', 'Rating Blocked shots':'Blocked<br>shots', 'Rating Interceptions':'Interceptions',
                                     'Rating Total tackles':'Total<br>tackles',"Rating Dribbled past":"Dribbled<br>past"})
                    .melt())
        try:
            gaugedef,stardef=st.columns([1,1])
            with gaugedef:
                gaugedefence=go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=defence.melt()['value'].mean().round(0),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={'axis': {'range': [None, 100]},
                                   'bordercolor': "gray"},
                            title={'text': "Defence<br>Rating<br>"}))

                gaugedefence.update_layout(
                            autosize=False,
                            width=200,
                            height=200,
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=70,
                                pad=0
                            ))

                st.write(gaugedefence)
            with stardef:
                stardef = go.Figure()
                stardef.add_trace(go.Barpolar(r=defencesel['value'],theta=defencesel['variable'],
                  name=selected_Player + " "+select_season+" "+select_phase+" "+select_round+" "+select_ha+" "+select_wl,marker_color='peru',
                    marker_line_color="black",
                    marker_line_width=2,
                    opacity=0.8,hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))


                stardef.update_layout(
                    width=300,
                    height=300,
                    showlegend=False,
                margin = dict(
                    l=50,
                    r=60,
                    b=10,
                    t=10,
                    pad=0
                ),
                    polar=dict(
                        radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
                        angularaxis=dict(showticklabels=True, ticks='')
                    )
                )
                st.write(stardef)
        except:
            st.error('No data available with these parameters')

        st.write("#### Duels Stats")
        totalduels, pergameduels = st.tabs(['Total', 'Per Game'])
        with totalduels:
            duels_stats_total = computeplayerstats_total_sel[
                ['Player', 'Duels', 'Duels won',  'Duels(%)','Ground duels', 'Ground duels won','Ground duels(%)', 'Aerial duels', 'Aerial duels won','Aerial duels(%)',
                 'Possession lost', 'Fouls', 'Was fouled']]
            interactive_table(
                duels_stats_total.set_index('Player'),
                paging=False, height=900, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])

        with pergameduels:
            duels_stats_mean = computeplayerstats_mean_sel[
                ['Player','Duels', 'Duels won',  'Duels(%)','Ground duels', 'Ground duels won','Ground duels(%)', 'Aerial duels', 'Aerial duels won','Aerial duels(%)',
                 'Possession lost', 'Fouls', 'Was fouled']]
            interactive_table(
                duels_stats_mean.set_index('Player'),
                paging=False, height=900, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])

        duels=players_ratings_sel[['Rating Duels', 'Rating Duels won',"Rating Duels(%)", 'Rating Ground duels', 'Rating Ground duels won','Rating Ground duels(%)', 'Rating Aerial duels',
                                'Rating Aerial duels won','Rating Aerial duels(%)','Rating Possession lost', 'Rating Fouls', 'Rating Was fouled']]

        duelssel=(duels[['Rating Duels won',"Rating Duels(%)", 'Rating Ground duels won','Rating Ground duels(%)','Rating Aerial duels won','Rating Aerial duels(%)',
                 'Rating Possession lost']]
                    .rename(columns={'Rating Duels won':'Duels<br>won', 'Rating Duels(%)':'Duels(%)', 'Rating Ground duels won':'Ground<br>duels<br>won',
                                     'Rating Ground duels(%)':'Ground<br>duels(%)',"Rating Aerial duels won":"Aerial<br>duels<br>won",'Rating Aerial duels(%)':'Aerial<br>duels(%)',
                                     'Rating Possession lost':'Possession<br>lost'})
                    .melt())
        try:
            gaugedue,stardue=st.columns([1,1])
            with gaugedue:
                gaugeduels=go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=duels.melt()['value'].mean().round(0),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={'axis': {'range': [None, 100]},
                                   'bordercolor': "gray"},
                            title={'text': "Duels<br>Rating<br>"}))

                gaugeduels.update_layout(
                            autosize=False,
                            width=200,
                            height=200,
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=70,
                                pad=0
                            ))


                st.write(gaugeduels)
            with stardue:
                stardue = go.Figure()
                stardue.add_trace(go.Barpolar(r=duelssel['value'],theta=duelssel['variable'],
                                              name=selected_Player + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl,
                                              marker_color='peru',
                                              marker_line_color="black",
                                              marker_line_width=2,
                                              opacity=0.8, hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))


                stardue.update_layout(
                    width=300,
                    height=300,
                    showlegend=False,
                margin = dict(
                    l=50,
                    r=60,
                    b=10,
                    t=10,
                    pad=0
                ),
                    polar=dict(
                        radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
                        angularaxis=dict(showticklabels=True, ticks='')
                    )
                )
                st.write(stardue)
        except:
            st.error('No data available with these parameters')
        st.write("#### Passing Stats")
        totalpass, pergamepass = st.tabs(['Total', 'Per Game'])
        with totalpass:
            passing_stats_total = computeplayerstats_total_sel[
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
            passing_stats_mean = computeplayerstats_mean_sel[
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
        passing=players_ratings_sel[['Rating Touches', 'Rating Accurate passes', 'Rating Total passes', "Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses',
                 'Rating Total Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls', 'Rating Total Long balls', "Rating Long balls(%)",
                 'Rating Big chances created','Rating Assists']]

        passsel=(passing[['Rating Touches', 'Rating Accurate passes',"Rating Passes(%)", 'Rating Key passes', 'Rating Accurate Crosses', "Rating Crosses(%)", 'Rating Accurate Long balls',
                         "Rating Long balls(%)",'Rating Big chances created']]
                    .rename(columns={'Rating Touches':'Touches', 'Rating Accurate passes':'Accurate<br>passes', 'Rating Passes(%)':'Passes(%)',
                                     'Rating Key passes':'Key<br>passes','Rating Accurate Crosses':"Accurate<br>Crosses",'Rating Crosses(%)':'Crosses(%)',
                                     'Rating Accurate Long balls':'Accurate<br>Long<br>balls',"Rating Long balls(%)":"Long<br>balls(%)",'Rating Big chances created':'Big<br>chances<br>created'})
                    .melt())
        try:
            gaugepass,starpass=st.columns([1,1])
            with gaugepass:
                gaugepass=go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=passing.melt()['value'].mean().round(0),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={'axis': {'range': [None, 100]},
                                   'bordercolor': "gray"},
                            title={'text': "Passing<br>Rating<br>"}))

                gaugepass.update_layout(
                            autosize=False,
                            width=200,
                            height=200,
                            margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=70,
                                pad=0
                            ))

                st.write(gaugepass)
            with starpass:
                starpass = go.Figure()
                starpass.add_trace(go.Barpolar(r=passsel['value'],theta=passsel['variable'],
                                               name=selected_Player + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl,
                                               marker_color='peru',
                                               marker_line_color="black",
                                               marker_line_width=2,
                                               opacity=0.8, hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))


                starpass.update_layout(
                    width=300,
                    height=300,
                    showlegend=False,
                margin = dict(
                    l=50,
                    r=60,
                    b=10,
                    t=10,
                    pad=0
                ),
                    polar=dict(
                        radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
                        angularaxis=dict(showticklabels=True, ticks='')
                    )
                )
                st.write(starpass)
        except:
            st.error('No data available with these parameters')
        st.write("#### Goalkeeping Stats")
        totalgk, pergamegk = st.tabs(['Total', 'Per Game'])
        with totalgk:
            goalkeeping_stats_total = computeplayerstats_total_sel[
                ['Player', 'Saves', 'Punches', 'Runs out succ', 'Runs out', 'High claims', 'Saves from inside box',
                 'Penalties saved']]
            interactive_table(
                goalkeeping_stats_total.set_index('Player'),
                paging=False, height=900, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])
        with pergamegk:
            goalkeeping_stats_mean = computeplayerstats_mean_sel[
                ['Player', 'Saves', 'Punches', 'Runs out succ', 'Runs out', 'High claims', 'Saves from inside box',
                 'Penalties saved']]
            interactive_table(
                goalkeeping_stats_mean.set_index('Player'),
                paging=False, height=900, width=2000, showIndex=True,
                classes="display order-column nowrap table_with_monospace_font", searching=True,
                fixedColumns=True, select=True, info=False, scrollCollapse=True,
                scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                columnDefs=[{"className": "dt-center", "targets": "_all"}])

        gk=players_ratings_sel[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box',
                 'Rating Penalties saved']]
        gksel=(gk[['Rating Saves', 'Rating Punches', 'Rating Runs out succ', 'Rating Runs out(%)', 'Rating High claims', 'Rating Saves from inside box']]
                    .rename(columns={'Rating Saves':'Saves', 'Rating Punches':'Punches', 'Rating Runs out succ':'Runs<br>out<br>succ',
                                     'Rating Runs out(%)':'Runs<br>out(%)','Rating High claims':"High<br>claims",'Rating Saves from inside box':'Saves<br>from<br>inside<br>box'})
                    .melt())

        try:
            gaugegk,stargk=st.columns([1,1])
            with gaugegk:
                gaugegk=go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=gk.melt()['value'].mean().round(0),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={'axis': {'range': [None, 100]},
                                   'bordercolor': "gray"},
                            title={'text': "Goalkeeping<br>Rating<br>"}))

                gaugegk.update_layout(
                        autosize=False,
                        width=200,
                        height=200,
                        margin=dict(
                            l=0,
                            r=0,
                            b=0,
                            t=70,
                            pad=0
                        ))

                st.write(gaugegk)
            with stargk:
                stargk = go.Figure()
                stargk.add_trace(go.Barpolar(r=gksel['value'],theta=gksel['variable'],
                  name=selected_Player + " " + select_season + " " + select_phase + " " + select_round + " " + select_ha + " " + select_wl,
                                           marker_color='peru',
                                           marker_line_color="black",
                                           marker_line_width=2,
                                           opacity=0.8, hovertemplate='%{theta} <br>Rating: %{r:.f}<extra></extra>'))

                stargk.update_layout(
                width=300,
                height=300,
                showlegend=False,
                margin = dict(
                l=50,
                r=60,
                b=10,
                t=10,
                pad=0
                ),
                polar=dict(
                    radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
                    angularaxis=dict(showticklabels=True, ticks='')
                )
                    )
                st.write(stargk)
        except:
            st.error('No data available with these parameters')
    except:
        st.error('No data available with these parameters')

with bygame:
    interactive_table(dataset_filter.loc[dataset_filter.Player == selected_Player][
                          ['Against', 'Season', 'Phase', 'Round', 'Fixture', 'Team', "Player", 'Minutes played',
                           'Goals', 'Assists', 'Yellow card', 'Red card',
                           'Shots on target',
                           'Shots off target', 'Shots blocked', 'Dribble attempts succ', 'Dribble attempts',
                           "Dribble(%)", 'Penalty won', 'Big chances missed',
                           'Penalty miss', 'Hit woodwork', 'Defensive actions',
                           'Clearances',
                           'Blocked shots', 'Interceptions', 'Total tackles',
                           'Dribbled past',
                           'Penalty committed', 'Own goals', 'Last man tackle',
                           'Error led to shot', 'Clearance off line',
                           'Error led to goal',
                           'Touches', 'Accurate passes', 'Total passes', "Passes(%)",
                           'Key passes', 'Accurate Crosses', 'Total Crosses', "Crosses(%)",
                           'Accurate Long balls', 'Total Long balls', "Long balls(%)", 'Big chances created',
                           'Duels won', 'Duels', "Duels(%)",
                           'Ground duels won', 'Ground duels', "Ground duels(%)", 'Aerial duels won', 'Aerial duels',
                           "Aerial duels(%)",
                           'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
                           'Punches', 'Runs out succ', 'Runs out', "Runs out(%)", 'High claims',
                           'Saves from inside box', 'Penalties saved']].set_index('Against'),
                      paging=False, height=900, width=2000, showIndex=True,
                      classes="display order-column nowrap table_with_monospace_font", searching=True,
                      fixedColumns=True, select=True, info=False, scrollCollapse=True,
                      scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
                      columnDefs=[{"className": "dt-center", "targets": "_all"}])
