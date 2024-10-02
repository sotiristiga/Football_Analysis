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

selected_ha = st.sidebar.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
selected_season = st.sidebar.selectbox("Season:",['All','2024-2025'],index=0)
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

selected_Player = st.sidebar.selectbox("Player:", dataset_filter['Player'].reset_index().sort_values('Player')['Player'].unique())



interactive_table(dataset_filter.loc[dataset_filter.Player==selected_Player][['Against','Season','Phase','Round','Fixture','Team',"Player",'Minutes played',
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
                                                           'Punches', 'Runs out succ','Runs out',  "Runs out(%)",'High claims','Saves from inside box','Penalties saved']].set_index('Against'),
        paging=False, height=900, width=2000, showIndex=True,
        classes="display order-column nowrap table_with_monospace_font", searching=True,
        fixedColumns=True, select=True, info=False, scrollCollapse=True,
        scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
        columnDefs=[{"className": "dt-center", "targets": "_all"}])
