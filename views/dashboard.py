import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import sys
sys.path.append("../")
from views.appointments import appointments
from views.courses import courses
from views.courses_history import courses_history
from views.notifications import notifications
from views.resources import resources
from views.settings import settings
from views.users import users

def logout():
    st.session_state.clear()
    switch_page("app")
    
def dash_info():
    pass

def dashboard():
    if "current_page" not in st.session_state:
        st.markdown("# Dashboard")
        st.session_state["current_page"] = "Dashboard"
    else:
        st.markdown(f'# {st.session_state["current_page"]}')

    if st.session_state["current_page"].__eq__("Appointments"):
        appointments()
    elif st.session_state["current_page"].__eq__("Courses"):
        courses()
    elif st.session_state["current_page"].__eq__("Course History"):
        courses_history()
    elif st.session_state["current_page"].__eq__("Notifications"):
        notifications()
    elif st.session_state["current_page"].__eq__("Resources"):
        resources()
    elif st.session_state["current_page"].__eq__("Settings"):
        settings()
    elif st.session_state["current_page"].__eq__("Users"):
        users()
    else:
        #dash
        dash_info()

    #sidebar
    st.sidebar.header("Dashboard")
    home_clicked = st.sidebar.button("Home", type="secondary", use_container_width=True)
    appointments_clicked = st.sidebar.button("Appointments", type="secondary", use_container_width=True)
    if(appointments_clicked):
        st.session_state["current_page"] = "Appointments"
        st.rerun()
    courses_clicked = st.sidebar.button("Courses", type="secondary", use_container_width=True)
    if(courses_clicked):
        st.session_state["current_page"] = "Courses"
        st.rerun()
    course_history_clicked = st.sidebar.button("Course History", type="secondary", use_container_width=True)
    if(course_history_clicked):
        st.session_state["current_page"] = "Course History"
        st.rerun()
    notifications_clicked = st.sidebar.button("Notifications", type="secondary", use_container_width=True)
    if(notifications_clicked):
        st.session_state["current_page"] = "Notifications"
        st.rerun()
    resources_clicked = st.sidebar.button("Resources", type="secondary", use_container_width=True)
    if(resources_clicked):
        st.session_state["current_page"] = "Resources"
        st.rerun()
    settings_clicked = st.sidebar.button("Settings", type="secondary", use_container_width=True)
    if(settings_clicked):
        st.session_state["current_page"] = "Settings"
        st.rerun()
    users_clicked = st.sidebar.button("Users", type="secondary", use_container_width=True)
    if(users_clicked):
        st.session_state["current_page"] = "Users"
        st.rerun()
    st.sidebar.divider()
    logout_clicked = st.sidebar.button("Logout", type="primary", use_container_width=True)

    if(logout_clicked):
        logout()
    st.container()