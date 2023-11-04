import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import ast

def company_overview_page(df, company_list):
    df_posts = pd.read_csv('data/combined_values.csv')
    st.header('Company Overview')
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    comp_list = filtered_df['edited_names']
    if filtered_df.empty == False:
        st.subheader('Company Investors')
        lgdf = filtered_df.groupby('Company').agg({'Lead Investor': lambda x: list(x)[0],'Other Investor': lambda x: list(set(x))[0]})
        st.table(lgdf)
        related = []
        for i,k in enumerate(comp_list):
            for j,l in zip(df_posts['post_name'],df_posts['slug']):
                if str(k) in str(l) or str(k) in str(j):
                    related.append(j)

        st.subheader('Investment Amount in Millions USD')
        fgdf = filtered_df[['Company','amount_usd','Country']].groupby(['Company']).sum()
        if len(fgdf['amount_usd']) > 1:
            #fgdf['amount_usd'].plot(kind = 'bar', ylabel = 'Amount in Millions')
            #st.pyplot()
            fig = px.bar(fgdf, x = fgdf.index, y = 'amount_usd',height=400, width = 700)
            fig.update_layout(title='Amount of Investments per Company', yaxis_title='Amount in Millions USD', xaxis_title='category')
            st.plotly_chart(fig)
        elif len(fgdf['amount_usd']) == 1:
            comp_val = list(fgdf['amount_usd'])[0]
            st.subheader(f':blue[The company {list(fgdf.index)[0]} has {comp_val} million USD.]')
        else:
            st.write('There is no investment amount found for the selected company')

        st.subheader('Related Articles')
        related_arts = df_posts[df_posts['post_name'].isin(related)][['post_title','post_name','guid','slug']].sort_values('post_title')
        if related_arts.empty:
            st.write('No articles related to this company')
        else:
            markdowntable = "| Article | Link | Company |\n| - | - | - |"
            for i,j,k,l in zip(related_arts['post_title'],related_arts['guid'],related_arts['slug'],related_arts['post_name']):
                if '.jpg' not in j and '.png' not in j:
                    if str(k) != 'nan':
                        comp = [a for a in ast.literal_eval(str(k)) if a in list(comp_list)]
                    if comp == []:
                        comp = [b for b in list(comp_list) if b in l]
                    markdowntable += f'\n| {i} | {j} | {comp[0]} |'
            st.markdown(markdowntable)


    else:
        st.write('Please Select a Company')
