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
from streamlit_extras.stylable_container import stylable_container

from models.User import User
from models.CourseHistory import CourseHistory
from models.Settings import Settings
from models.Appointment import Appointment

def logout():
    st.session_state.clear()
    switch_page("app")

def dash_info():
    user = User.get_current_user_details(st)
    settings = Settings.getSettings()
    if user is None:
        st.error("Not logged in!")
    else:
        st.session_state["my_courses"] = CourseHistory.getCoursesByStudent(user.getUid())
        current = []
        for course in st.session_state["my_courses"]:
            if course["year"].__eq__(str(settings.getCurrentYear())) and course["semester"].__eq__(settings.getCurrentSemester()):
                current.append(course)

        card1, card2 = st.columns(2)
        with card1:
            with stylable_container("tcourses", css_styles="""
                {
                    border: 1px solid white;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                }
                """):
                st.header("Total Courses", divider=True)
                st.write(str(len(st.session_state["my_courses"])))

        with card2:
            with stylable_container("tcourses", css_styles="""
            {
                border: 1px solid white;
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
            }
            """):
                st.header("Currrent Courses", divider=True)
                st.write(str(len(current)))

        #appointments
        st.session_state["appointments"] = Appointment.getAppointments(user.getUid())
        st.markdown("# My Appointments")
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


def dashboard():
    if "current_page" not in st.session_state:
        st.markdown("# Dashboard")
        st.session_state["current_page"] = "Dashboard"
    else:
        st.markdown(f'# {st.session_state["current_page"]}')

    if st.session_state["current+page"].__eq__("Dashboard"):
        dash_info()
    elif st.session_state["current_page"].__eq__("Appointments"):
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
    if home_clicked:
        st.session_state["current_page"] = "Dashboard"
        st.rerun()
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