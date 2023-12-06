import streamlit as st
import sys
sys.path.append("../")

from datetime import datetime
import pandas as pd
import numpy as np
import re

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from models.Appointment import Appointment
from models.User import User

def formatUserName(option):
    return f'{option["fName"]} {option["lName"]}'

#get current user
user = User.get_current_user_details(st)
if user is None:
    st.error("Not logged in!")
else:
    #fetch users
    st.session_state["all_users"] = User.getAllUsers()

    ##display received and sent appointments in tabs
    list ,form = st.tabs(["Users", "Edit User"])

    with list:
        if st.button("Reload", key=4):
            st.rerun()

        df = pd.DataFrame.from_records(st.session_state["all_users"])
        df.index = np.arange(1, len(df)+1)
        selected_rows = [] if 'selected_user_row' not in st.session_state else st.session_state['selected_user_row']
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, wrapText=False, autoHeight=True)
        gb.configure_column('fName', headerName="First Name", minWidth=200, maxWidth=200)
        gb.configure_column('lName', headerName="Last Name", minWidth=200, maxWidth=200)
        gb.configure_column('email', headerName="Email Address", minWidth=200, maxWidth=200)
        gb.configure_column('phone', headerName="Phone Number", minWidth=200, maxWidth=200)
        gb.configure_column('role', headerName="Role", minWidth=200, maxWidth=200)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=3)
        gb.configure_side_bar()
        gb.configure_selection('single', pre_selected_rows=selected_rows, use_checkbox=True)
        gb_grid_options = gb.build()
        
        grid_return = AgGrid(df,gridOptions = gb_grid_options,
            key = 'uid',
            reload_data = True,
            data_return_mode = DataReturnMode.AS_INPUT,
            update_mode = GridUpdateMode.MODEL_CHANGED, # GridUpdateMode.SELECTION_CHANGED or GridUpdateMode.VALUE_CHANGED or 
            fit_columns_on_grid_load = True,
            height = 350,
            width = '100%',
            theme = "streamlit")

        selected_rows = grid_return["selected_rows"]
        print("Selected Row: ", selected_rows)
        st.session_state['selected_user_row'] = selected_rows

    with form:
        form_valid = True
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        st.markdown("Save User Account")
        with st.form("user_form"):
            fName = st.text_input("First Name", "", type="default")
            lName = st.text_input("Last Name", "", type="default")
            email = st.text_input("Email Address", "", type="default")
            phone = st.text_input("Phone Number", "", type="default")
            role = st.selectbox("Role", ['Admin', "Student", "Advisor"])
            password = st.text_input("Password", "", type="password")
            confirm_password = st.text_input("Confirm Password", "", type="password")

            submitted = st.form_submit_button("Save Details")
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