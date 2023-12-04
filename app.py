""" Entry point of app
"""
import streamlit as st
from LoginForm import login_form

def is_logged_in():
    if "authenticated" not in st.session_state:
        return False
    else:
        if st.session_state["authenticated"]:
            authenticate = True
        else:
            return False

if is_logged_in():
    # dashboard
    dashboard()
else:
    login_form()