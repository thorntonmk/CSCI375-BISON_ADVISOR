import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def logout():
    st.session_state.clear()
    switch_page("app")
    


st.markdown("# Dashboard")
st.sidebar.header("Dashboard")

logout_clicked = st.sidebar.button("Logout")
if(logout_clicked):
    logout()
st.container()