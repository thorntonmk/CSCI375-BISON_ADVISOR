import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import sys
sys.path.append("../")

import pandas as pd
import numpy as np

from models.Course import Course
from models.Settings import Settings
from models.User import User

def courses():
    clist, cform, cRegister = st.tabs(["Courses", "Edit Course", "Register For Courses"])

    st.session_state["all_courses"] = Course.courses_to_json()

    with clist:
        st.header("Courses List")
        if st.button("Reload"):
            st.rerun()
        df = pd.DataFrame.from_records(st.session_state["all_courses"])
        df.index = np.arange(1, len(df)+1)
        selected_rows = [] if 'selected_course_row' not in st.session_state else st.session_state['selected_course_row']
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, wrapText=False, autoHeight=True)
        gb.configure_column('code', minWidth=200, maxWidth=200)
        gb.configure_column('name', minWidth=200, maxWidth=200)
        gb.configure_column('prerequisites', minWidth=200, maxWidth=400)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=3)
        gb.configure_side_bar()
        gb.configure_selection('single', pre_selected_rows=selected_rows, use_checkbox=True)
        gb_grid_options = gb.build()
        
        grid_return = AgGrid(df,gridOptions = gb_grid_options,
            key = 'code',
            reload_data = True,
            data_return_mode = DataReturnMode.AS_INPUT,
            update_mode = GridUpdateMode.MODEL_CHANGED, # GridUpdateMode.SELECTION_CHANGED or GridUpdateMode.VALUE_CHANGED or 
            fit_columns_on_grid_load = True,
            height = 500,
            width = '100%',
            theme = "streamlit")

        selected_rows = grid_return["selected_rows"]
        print("selected row: ", selected_rows)
        if(len(selected_rows) > 0):
            st.session_state['selected_course_row'] = selected_rows

    with cform:
        st.header("Save Course Details")
        form_valid = False
        if "selected_course_row" not in st.session_state or st.session_state["selected_course_row"] is None:
            data = {
                "code": "",
                "name": "",
                "prerequisites": []
            }
        else:
            data = {
                "code": st.session_state["selected_course_row"][0]["code"],
                "name": st.session_state["selected_course_row"][0]["name"],
                "prerequisites": st.session_state["selected_course_row"][0]["prerequisites"],
            }
        with st.form("courses_form", clear_on_submit=True):
            code = st.text_input("Course Code", data['code'], type="default")
            name = st.text_input("Course Name", data['name'], type="default")
            prereqs = st.multiselect("Prerequisites", default=[] if data['prerequisites'] is None else data['prerequisites'], options=[c["code"] for c in st.session_state["all_courses"]])
            
            submitted = st.form_submit_button("Save Course")
            if(submitted):
                form_valid = True
                if code == None:
                    form_valid = False
                    st.error("Code is required")
                
                if name == None:
                    form_valid = False
                    st.error("Name is required")
                
                
                if not form_valid:
                    st.error("Fix all issues then try again")
                else:
                    course = Course()
                    course.setCode(code)
                    course.setName(name)
                    course.setPrerequisites(prereqs)

                    result = course.saveCourse()
                    if not result:
                        st.error("Could not create course")
                    else:
                        st.success("Course created successfully")
                        st.session_state["all_courses"] = Course.courses_to_json()
                        st.session_state["selected_course_row"] = None
            
            
        delete = st.button("Delete Course")
        if delete:
            deleted = Course.delete_course(course_code=data["code"])
            if deleted:
                st.success("Deleted Successfully")
                st.session_state["all_courses"] = Course.courses_to_json()
                st.session_state["selected_course_row"] = None
            else:
                st.error("Could not delete. Course does not exist")

    with cRegister:
        def formatcourse(option):
            return f'{option["name"]}'
        if "current_settings" not in st.session_state:
            st.session_state["current_settings"] = Settings.getSettings()
        
        c_period_container = st.container()

        with c_period_container:
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Current Year", str(st.session_state["current_settings"].getCurrentYear()), disabled=True)
            with col2:
                st.text_input("Current Semester", f'{st.session_state["current_settings"].getCurrentSemester()} Semester', disabled=True)

            if "authenticated" not in st.session_state:
                st.error("Not Logged in!")
            else:
                def formatUser(option):
                    return f'{option["fName"]} {option["lName"]}'
                currentUser = User.getUser(st.session_state["current_user_id"])
                currentCourses = Course.courses_to_json()
                if currentUser.getRole().__eq__("Admin"):
                    student = st.selectbox("Select A Student", options=User.get_students(), index=None, format_func=formatUser, placeholder="Select one")
                    course = st.selectbox("Select A Course", options=currentCourses, index=None, format_func=formatcourse, placeholder="Select one")

                    register = st.button("Register Course")
                    if register:
                        if student is None:
                            st.error("Student is required")
                        elif course is None:
                            st.error("Course is required")
                        else:
                            res = Course.register_student_for_course(currentUser.getUid(), course["code"], course["prerequisites"])
                            if type(res) == str:
                                st.error(res)
                            else:
                                st.success("Course registered successfully")

                else:
                    st.text_input("Student", f'{currentUser.getFName()} {currentUser.getLName()}', disabled=True)
                    course = st.selectbox("Select A Course", options=currentCourses, format_func=formatcourse, index=None, placeholder="Select one")

                    register = st.button("Register Course")
                    if register:
                        if course is None:
                            st.error("Course is required")
                        else:
                            res = Course.register_student_for_course(currentUser.getUid(), course["code"], course["prerequisites"])
                            if type(res) == str:
                                st.error(res)
                            else:
                                st.success("Course registered successfully")
        
