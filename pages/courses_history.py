import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import sys
sys.path.append("../")

import pandas as pd
import numpy as np

from models.CourseHistory import CourseHistory
from models.Course import Course
from models.User import User

clist, cform = st.tabs(["List", "Form"])

st.session_state["all_courses"] = Course.courses_to_json()
st.session_state["all_students"] = User.get_students()

def formatStudentSelect(option):
    return f'{option["fName"]} {option["lName"]}'

def formatCourseSelect(option):
    return option["name"]

def findCourseIndex(code):
    idx = -1
    for course in st.session_state["all_courses"]:
        if course["code"].__eq__(code):
            break
        else:
            idx += 1
    return idx

with clist:
    st.header("Courses History")
    if st.button("Reload"):
        st.rerun()
    
    selected_student = st.selectbox("Select Student", 
                                    options=st.session_state["all_students"],
                                    format_func=formatStudentSelect,
                                    index=None,
                                    placeholder="---Select a student---")
    
    #get data from selected student
    st.session_state["selected_student"] = selected_student
    if st.session_state["selected_student"]:
        st.session_state["student_courses"] = CourseHistory.getCoursesByStudent(st.session_state["selected_student"]["uid"])
    else:
        st.session_state["student_courses"] = []
    
    df = pd.DataFrame.from_records(st.session_state["student_courses"])
    df.index = np.arange(1, len(df)+1)
    selected_rows = [] if 'selected_course_history_row' not in st.session_state else st.session_state['selected_course_history_row']
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, wrapText=False, autoHeight=True)
    gb.configure_column('course', headerName="Course", minWidth=200, maxWidth=200)
    gb.configure_column('year', headerName="Student Year", minWidth=200, maxWidth=200)
    gb.configure_column('semester', headerName="Semester", minWidth=200, maxWidth=200)
    gb.configure_column('assignmentTotal', headerName="Assignment Total", minWidth=200, maxWidth=200)
    gb.configure_column('midtermTotal', headerName="Midterm Total", minWidth=200, maxWidth=200)
    gb.configure_column('finalTotal', headerName="FInal Total", minWidth=200, maxWidth=200)
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
        height = 500,
        width = '100%',
        theme = "streamlit")

    selected_rows = grid_return["selected_rows"]
    print("Selected Row: ", selected_rows)
    st.session_state['selected_course_history_row'] = selected_rows

with cform:
    st.header("Save Course Details")
    sems = ["Fall", "Spring", "Summer", "Winter"]
    form_valid = False
    if "selected_course_history_row" not in st.session_state or len(st.session_state["selected_course_history_row"]) == 0:
        data = {
            "course": "",
            "student": "",
            "year": 2010,
            "semester": 1,
            "assignmentTotal": 0,
            "midtermTotal": 0,
            "finalTotal": 0
        }
    else:
        data = {
            "course": st.session_state["selected_course_history_row"][0]["course"],
            "student": st.session_state["selected_student"]["uid"],
            "year": int(st.session_state["selected_course_history_row"][0]["year"]),
            "semester": st.session_state["selected_course_history_row"][0]["semester"],
            "assignmentTotal": int(st.session_state["selected_course_history_row"][0]["assignmentTotal"]),
            "midtermTotal": int(st.session_state["selected_course_history_row"][0]["midtermTotal"]),
            "finalTotal": int(st.session_state["selected_course_history_row"][0]["finalTotal"])
        }
    with st.form("courses_form", clear_on_submit=True):
        student = st.text_input("Student", 
                                f'{st.session_state["selected_student"]["fName"]} {st.session_state["selected_student"]["lName"]}' if st.session_state["selected_student"] else "",
                                disabled=True)
        course = st.selectbox("Select Course", 
                            options=st.session_state["all_courses"],
                            format_func=formatCourseSelect,
                            index=findCourseIndex(data["course"]),
                            placeholder="---Select a course---")
        year = st.selectbox("Year", range(2000, 2031), index=range(2000, 2031).index(data["year"]), placeholder="---Select an year---")
        semester = st.selectbox("Semester", sems, index=sems.index(data["semester"]), placeholder="---Select a semester---")
        assignmentTotal = st.number_input("Assignment Total", min_value=0, max_value=100, step=1, value=data["assignmentTotal"])
        midtermTotal = st.number_input("Midterm Total", min_value=0, max_value=100, step=1, value=data["midtermTotal"])
        finalTotal = st.number_input("Final Total", min_value=0, max_value=100, step=1, value=data["finalTotal"])
        
        
        submitted = st.form_submit_button("Save History")
        if(submitted):
            form_valid = True
            if course is None:
                form_valid = False
                st.error("Course is required")
            
            if year is None:
                form_valid = False
                st.error("Year is required")
            
            if semester is None:
                form_valid = False
                st.error("Semester is required")
            
            if assignmentTotal is None:
                form_valid = False
                st.error("Assignment Total is required")
            
            if midtermTotal is None:
                form_valid = False
                st.error("Midterm Total is required")

            if finalTotal is None:
                form_valid = False
                st.error("Final Total is required")
            
            if not form_valid:
                st.error("Fix all issues and try again")
            else:
                courseH = CourseHistory()
                courseH.setStudentId(st.session_state["selected_student"]["uid"])
                courseH.setCourseId(course["code"])
                courseH.setAssignmentTotal(assignmentTotal)
                courseH.setMidTermTotal(midtermTotal)
                courseH.setFinalTotal(finalTotal)
                courseH.setSemester(semester)
                courseH.setYear(year)

                try:
                    result = courseH.saveData()
                    if result:
                        st.success("Saved Successfully")
                    else:
                        st.error("Could not save data successfully")
                except ValueError as e:
                    st.error("Student has done this course")
        
        
    delete = st.button("Delete History", disabled=True if "selected_course_history_row" not in st.session_state else False)
    if delete:
        deleted = CourseHistory.deleteStudentCourse(st.session_state["selected_course_history_row"][0]["uid"])
        if deleted:
            st.success("Deleted Successfully")
            st.session_state["student_courses"] = CourseHistory.getCoursesByStudent(st.session_state["selected_student"]["uid"])
            st.session_state["selected_course_history_row"] = []
        else:
            st.error("Could not delete. History does not exist")
