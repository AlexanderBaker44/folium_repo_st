import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

def general_overview_page(metric_dict, df):
    st.header('General Financial Analysis')
    selected_metric_m = st.selectbox(label = 'Select Metric',options = ['Number of Investments','Amount in Millions USD'])
    selected_metric = metric_dict[selected_metric_m]


    if selected_metric_m == 'Number of Investments':
        time_investor = df.dropna().groupby('Month').count()['Unnamed: 0']

        by_type = df.groupby('Major Category').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector = df.groupby('Subcategory').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']


        by_type_s = df.dropna().groupby('Strategics').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector_s = df.dropna().groupby('Stage').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        selected_metric_s = 'Unnamed: 0'


    elif selected_metric_m == 'Amount in Millions USD':
        #print(selected_metric_m)
        time_investor = df.dropna().groupby('Month').sum()['amount_usd']
        print(time_investor)
        by_type = df[['Major Category','amount_usd']].groupby('Major Category').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector = df[['Subcategory','amount_usd']].groupby('Subcategory').sum().sort_values('amount_usd',ascending=False)['amount_usd']


        by_type_s = df[['Strategics','amount_usd']].dropna().groupby('Strategics').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector_s = df[['Stage','amount_usd']].dropna().groupby('Stage').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        selected_metric_s = metric_dict[selected_metric_m]


    st.subheader('Monthly Analysis')
    #figt, mnxt = plt.subplots(1, 1)
    #time_investor.plot(kind = 'line', figsize = (20,10), title = 'Investments Made Over Time', ylabel = f'{selected_metric_m}')
    #st.pyplot()
    fig = px.line(time_investor, x = time_investor.index, y = selected_metric_s,height=400, width = 800)
    fig.update_layout(title='Time Analysis', yaxis_title=selected_metric_m, xaxis_title='month')
    st.plotly_chart(fig)


    st.subheader('Investor Categories')
    col1,col2 = st.columns(2)
    with col1:
        #figmx, mnx = plt.subplots(1, 1)
        #by_type.plot(ax = mnx, kind = 'bar',title = 'Investments by Category', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_type, x = by_type.index, y = selected_metric_s,height=400, width = 400)
        fig.update_layout(title='Category', yaxis_title=selected_metric_m, xaxis_title='category')
        st.plotly_chart(fig)

    with col2:
        #figmxv, mnxv = plt.subplots(1, 1)
        #by_sector.plot(ax = mnxv, kind = 'bar',title = 'Investments by Subcategory', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_sector, x = by_sector.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Subcategory', yaxis_title=selected_metric_m, xaxis_title='subcategory')
        st.plotly_chart(fig)

    st.subheader('Additional Investment Information')
    col1,col2 = st.columns(2)
    with col1:
        #by_sector_s.plot(kind = 'bar',title = 'Investments by Stage', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_sector_s, x = by_sector_s.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Stage', yaxis_title=selected_metric_m, xaxis_title='stage')
        st.plotly_chart(fig)
    with col2:
        #by_type_s.plot(kind = 'bar',title = 'If Investment is Strategic', ylabel = f'{selected_metric_m}')
        #st.pyplot()
        fig = px.bar(by_type_s, x = by_type_s.index, y = selected_metric_s, height=400, width = 400)
        fig.update_layout(title='Strategics', yaxis_title=selected_metric_m, xaxis_title='strategics')
        st.plotly_chart(fig)
