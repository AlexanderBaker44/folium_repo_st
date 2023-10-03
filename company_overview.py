import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

def company_overview_page(df, company_list):
    st.header('Company Overview')
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    if filtered_df.empty == False:
        st.subheader('Company Investors')
        lgdf = filtered_df.groupby('Company').agg({'Lead Investor': lambda x: list(x)[0],'Other Investor': lambda x: list(set(x))[0]})
        st.table(lgdf)

        st.subheader('Investment Amount in Millions USD')
        fgdf = filtered_df[['Company','amount_usd','Country']].groupby(['Company']).sum()
        if len(fgdf['amount_usd']) > 1:
            #fgdf['amount_usd'].plot(kind = 'bar', ylabel = 'Amount in Millions')
            #st.pyplot()
            fig = px.bar(fgdf, x = fgdf.index, y = 'amount_usd',height=400, width = 800)
            fig.update_layout(title='Amount of Investments per Company', yaxis_title='Amount in Millions USD', xaxis_title='category')
            st.plotly_chart(fig)
        elif len(fgdf['amount_usd']) == 1:
            comp_val = list(fgdf['amount_usd'])[0]
            st.markdown(f'#### The company {list(fgdf.index)[0]} has {comp_val} million USD.')
        else:
            st.write('There is no investment amount found for the selected company')
    else:
        st.write('Please Select a Company')
