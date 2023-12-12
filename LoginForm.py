import streamlit as st
from firebase import firebase
import re
import sys
sys.path.append("../")
from models.User import User
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
from streamlit_extras.switch_page_button import switch_page

auth = firebase.auth()

st.set_page_config(initial_sidebar_state="collapsed")

def login_form():
    st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("# Login to BisonAdvisor")

    with st.form("loginform"):
        st.write("Login to Bison Advisor")
        email = st.text_input("Email Address", "", type="default")
        password = st.text_input("Password", "", type="password")

        submitted = st.form_submit_button("Login")
        if(submitted):
            form_valid = True
            if email == None:
                form_valid = False
                st.error("Email Address is required")
            elif not re.match(email_regex, email):
                form_valid = False
                st.error("Please Provide a valid email address")
            
            if password == None:
                form_valid = False
                st.error("Password is required")
            
            if not form_valid:
                st.error("Fix all issues then try again")
                return False
            else:
                result = User.login(email, password)
                if result:
                    st.success("Logged in successfully")
                    st.session_state["current_user_id"] = result
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect email or password")
                    st.session_state["authenticated"] = False
        
                    