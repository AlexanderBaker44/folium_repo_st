import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from general_overview import general_overview_page
from company_overview import company_overview_page
from geographical_overview import geographical_page
#new comment
#from folium_mapping_sample import df_geo, create_map, cont_dict, continent_list
import folium
import branca
from streamlit_folium import st_folium
from folium.features import GeoJsonPopup, GeoJsonTooltip

#renderng glitch has to do with tabs
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('data/preprocessed_funding.csv')

ddf = df
ddf['Month'] = pd.to_datetime(ddf['Month'])

#df_geo = gpd.read_file("data/edited_geo_df.shp")
#print(df_geo)
df_geo = gpd.read_file("data/edited_geo_df.shp")
filtered_geo = df_geo.dropna(subset = ['amount_usd'])
company_list = list(set(df['Company']))
#continent_list = list(set(filtered_geo['continent']))


metric_dict = {'Count':'count', 'Amount in Millions':'amount_usd'}
cont_dict = {
'World': [[-50.003431,-175.781123],[78.091047,188.676738]],
'North America': [[-2.600651,-130.909825],[69.778954,-63.856951]],
#'South America': [[-58.704332,-89.218864],[9.726405,-28.006829]],
'Africa': [[-37.020096,-15.406895],[36.738886,40.176447]],
'Europe': [[33.049188,-21.598470],[70.104502,49.111984]],
'Asia': [[7.536767,32.480595],[54.876608,150.260988]],
'Oceania': [[-41.692597,96.366250],[6.070650,187.128922]]
}


continent_list = list(cont_dict.keys())


metric_dict = {'Number of Investments':'count', 'Amount in Millions USD':'amount_usd'}

with st.sidebar:
    page  = st.radio('Choose Page', ('General', 'Company Overview', 'Geographic'))
#tabs general, geographic, single companies
#tab1,tab2,tab3 = st.tabs(['General','Company Overview','Geographic'])

#general metrics count and total
if page == 'General':
    general_overview_page(metric_dict, df)

#geographic, count and total toggle

#selected_metric = st.dropdown()

if page == 'Company Overview':
    company_overview_page(df,company_list)

if page  == 'Geographic':
    geographical_page(df_geo, metric_dict, continent_list, cont_dict)



#single company all info written
#selected_companies = st.multiselect()


# Using object notation
