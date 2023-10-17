import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
#new comment
#from folium_mapping_sample import df_geo, create_map, cont_dict, continent_list
import folium
import branca
from streamlit_folium import st_folium
from folium.features import GeoJsonPopup, GeoJsonTooltip


def geographical_page(df_geo, metric_dict,continent_list, cont_dict):
    st.header('Geography Dashboard')
    metric_name = st.selectbox(label = 'Select Geographic Metric',options = ['Number of Investments','Amount in Millions USD'])
    metric = metric_dict[metric_name]
    selected_continent =  st.selectbox('Select Geographic Body to Analyze', options = continent_list)
    m = folium.Map()
    st.subheader('Map')
    #print(selected_continent)
    m.fit_bounds(cont_dict[selected_continent])

    if selected_continent == 'World':
        fcdf = df_geo
    else:
        fcdf = df_geo[df_geo['continent'] == selected_continent]

    colormap = branca.colormap.LinearColormap(
        vmin=fcdf[metric].quantile(0.0),
        vmax=fcdf[metric].quantile(1),
        colors=["red", "blue"],
        caption=metric_name,
    )
    popup = GeoJsonPopup(
        fields=["name", metric],
        aliases=["Country: ", f'{metric_name}: '],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = GeoJsonTooltip(
        fields=["name", metric],
        aliases=["Country: ", f'{metric_name}: '],
        localize=True,
        sticky=True,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )


    folium.GeoJson(
        fcdf,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"][metric])
            if x["properties"][metric] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    colormap.add_to(m)


    m.fit_bounds(cont_dict[selected_continent])



    st_data = st_folium(m, height = 400, width=700)
    df_bar = fcdf[['name',metric]].dropna().sort_values(metric ,ascending = False)

    st.subheader('Numerical Comparison')
    if len(df_bar['name']) > 1:
        fig = px.bar(df_bar, x = 'name', y = metric,height=400, width = 700)
        fig.update_layout(title='Amount per Country', yaxis_title= metric_name, xaxis_title='country')
        st.plotly_chart(fig)
    elif len(df_bar['name']) == 1:
        cont_val = list(df_bar[metric])[0]
        name_cont = list(df_bar['name'])[0]
        if metric == 'amount_usd':
            st.subheader(f':blue[The country {name_cont} has {cont_val} invested in millions USD.]')
        elif metric == 'count':
            st.subheader(f':blue[The country {name_cont} has an investment count of {int(cont_val)}.]')
    else:
        st.write('Continent has no relevant investments.')
