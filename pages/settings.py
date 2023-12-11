import streamlit as st
import sys
sys.path.append("../")

from datetime import datetime
import pandas as pd
import numpy as np
import re

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from models.Appointment import Appointment
from models.Settings import Settings

#get current user
settings = Settings.getSettings()

st.header("Settings")

container = st.container()
def getSemIndex(semesters, sem):
    count = 0
    for s in semesters:
        if s.__eq__(sem):
            break
        else:
            count += 1
    return count

with container:
    semesters = ["Fall", "Spring", "Summer"]
    current_year = st.number_input("Current Year", value=settings.getCurrentYear(), min_value=2000, max_value=9999)
    current_sem = st.selectbox("Current Semester", options=semesters, index=getSemIndex(semesters, settings.getCurrentSemester()))

    update = st.button("Update Settings", type="secondary")
    if update:
        settings.setCurrentYear(current_year)
        settings.setCurrentSemester(current_sem)
        settings.saveData()
        st.success("saved successfully")