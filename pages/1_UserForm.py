import streamlit as st
import re

import sys
sys.path.append("../")

from models.User import User

form_valid = True
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
st.markdown("# Create User Account")
st.sidebar.header("Create User Account")
with st.form("user_form"):
    st.write("Create User Account")
    fName = st.text_input("First Name", "", type="default")
    lName = st.text_input("Last Name", "", type="default")
    email = st.text_input("Email Address", "", type="default")
    phone = st.text_input("Phone Number", "", type="default")
    role = st.selectbox("Role", ['Admin', "Student", "Advisor"])
    password = st.text_input("Password", "", type="password")
    confirm_password = st.text_input("Confirm Password", "", type="password")

    submitted = st.form_submit_button("Create Details")
    if(submitted):
        form_valid = True
        if fName == None:
            form_valid = False
            st.error("First Name is required")
        
        if lName == None:
            form_valid = False
            st.error("Last Name is required")
        
        if email == None:
            form_valid = False
            st.error("Email Address is required")
        elif not re.match(email_regex, email):
            form_valid = False
            st.error("Please Provide a valid email address")
        
        if phone == None:
            form_valid = False
            st.error("phone Number is required")

        if role == None:
            form_valid = False
            st.error("Role is required")

        if password == None:
            form_valid = False
            st.error("Password is required")
        
        if confirm_password == None:
            form_valid = False
            st.error("Confirm Password is required")
        
        if not password.__eq__(confirm_password):
            form_valid = False
            st.error("Passwords do not match")
        
        if not form_valid:
            st.error("Fix all issues then try again")
        else:
            user = User()
            user.setFName(fName)
            user.setLName(lName)
            user.setEmail(email)
            user.setPhone(phone)
            user.setPassword(password)
            user.setRole(role)

            result = user.createUser()
            if not result:
                st.error("Could not create user: Email already exists")
            else:
                st.success("User created successfully")