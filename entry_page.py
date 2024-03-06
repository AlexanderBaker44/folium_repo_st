import streamlit as st

def entry_page_func():
    st.header("Space Intel Report Financials Dashboard")
    st.write('')
    st.subheader('Dashboard Overview')
    st.markdown(
                '''
                This dashboard provides insight into the financials, and investing rounds of various companies.
                Navigate the dashboard using sidebar to the left:
                * General - Displays general financial statistics.
                * Company Overview - Displays information about selected companies.
                * Geographic - Displays information along geographic lines.
                '''
                )
