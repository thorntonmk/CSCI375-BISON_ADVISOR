import streamlit as st
from app import firebase

auth = firebase.auth()

st.markdown("# Create User Account")
st.sidebar.header("Create User Account")

print(auth.current_user)