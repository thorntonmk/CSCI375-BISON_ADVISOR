import streamlit as st
import sys
sys.path.append("../")

from datetime import datetime

from models.Appointment import Appointment
from models.User import User

def formatUserName(option):
    return f'{option["fName"]} {option["lName"]}'

def appointments():
    #get current user
    user = User.get_current_user_details(st)
    if user is None:
        st.error("Not logged in!")
    else:
        #fetch appointments
        st.session_state["appointments"] = Appointment.getAppointments(user.getUid())
        st.session_state["all_users"] = User.getAllUsers()

        ##display received and sent appointments in tabs
        all ,received, sent, send = st.tabs(["All Appointments", "Received Requests", "Sent Appointments", "Make new Appointment"])

        with all:
            if st.button("Reload", key=4):
                st.rerun()

            for appointment in st.session_state["appointments"]["received"]:
                cont = st.container()
                with cont:
                    st.write(appointment["description"])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        usr = User.getUser(appointment["appointer"])
                        st.write(f'From: {usr.getFName()} {usr.getLName()}')
                    with col2:
                        st.write(f'Confirmed: {appointment["confirmed"]}')
                    with col3:
                        st.write(f'{appointment["date"]} {appointment["time"]}')
                st.divider()
            
            for appointment in st.session_state["appointments"]["sent"]:
                cont = st.container()
                with cont:
                    st.write(appointment["description"])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        usr = User.getUser(appointment["appointer"])
                        st.write(f'From: {usr.getFName()} {usr.getLName()}')
                    with col2:
                        st.write(f'Confirmed: {appointment["confirmed"]}')
                    with col3:
                        st.write(f'{appointment["date"]} {appointment["time"]}')
                st.divider()

        with received:
            if st.button("Reload", key=1):
                st.rerun()
            count = 0
            for appointment in st.session_state["appointments"]["received"]:
                cont = st.container()
                with cont:
                    st.write(appointment["description"])
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        usr = User.getUser(appointment["appointer"])
                        st.write(f'From: {usr.getFName()} {usr.getLName()}')
                    with col2:
                        st.write(f'Confirmed: {appointment["confirmed"]}')
                    with col3:
                        st.write(f'{appointment["date"]} {appointment["time"]}')
                    with col4:
                        btn = st.button("Confirm Appointment", key=count, disabled=appointment["confirmed"])
                        if btn:
                            Appointment.ConfirmAppointment(appointment["uid"])
                count += 1
                st.divider()

        with sent:
            if st.button("Reload", key=2):
                st.rerun()

            for appointment in st.session_state["appointments"]["sent"]:
                cont = st.container()
                with cont:
                    st.write(appointment["description"])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        usr = User.getUser(appointment["appointee"])
                        st.write(f'To: {usr.getFName()} {usr.getLName()}')
                    with col2:
                        st.write(f'Confirmed: {appointment["confirmed"]}')
                    with col3:
                        st.write(f'{appointment["date"]} {appointment["time"]}')
                st.divider()
        
        with send:
            st.header("Create Appointment")
            form_valid = False
        
            with st.form("appointments_form", clear_on_submit=False):
                to = st.selectbox("Recepient", st.session_state["all_users"], format_func=formatUserName, index=None, placeholder="---Select a recepient---", disabled=False if user.getRole().__eq__("Admin") else True)
                message = st.text_area("Description", 
                                        "",disabled=False if user.getRole().__eq__("Admin") else True)
                date = st.date_input("Date", 
                                    value="today",
                                    min_value=datetime.now(),
                                    format="DD/MM/YYYY"
                                    )
                time = st.time_input("Time", value="now")
                
                confirmed = st.checkbox("Confirm Appointment", False)
                
                
                
                submitted = st.form_submit_button("Send Notification")
                if(submitted):
                    form_valid = True
                    if message is None:
                        form_valid = False
                        st.error("message is required")
                    
                    if date is None:
                        form_valid = False
                        st.error("date is required")

                    if time is None:
                        form_valid = False
                        st.error("time is required")
                    
                    if to is None:
                        form_valid = False
                        st.error("recepient is required")
                    
                    if not form_valid:
                        st.error("Fix all issues and try again")
                    else:
                        appt = Appointment()
                        appt.setDescription(message)
                        appt.setDate(date.strftime('%d/%m/%Y'))
                        appt.setAppointee(to["uid"])
                        appt.setAppointer(st.session_state["current_user_id"])
                        appt.setTime(time.strftime("%H:%M:%S"))
                        appt.setConfirmed(confirmed)

                        try:
                            result = appt.saveData()
                            if result:
                                st.success("Saved Successfully")
                            else:
                                st.error("Could not make appointment")
                        except ValueError as e:
                            st.error("An error occured while trying to make this appointment")