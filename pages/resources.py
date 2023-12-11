import streamlit as st
import sys
sys.path.append("../")

from datetime import datetime
import pandas as pd
import numpy as np
import re

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from models.Settings import Settings
from models.Storage import Storage

#get current user
settings = Settings.getSettings()

st.header("Rsources")

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
    name = st.number_input("Current Year", value=settings.getCurrentYear(), min_value=2000, max_value=9999)
    folder = st.selectbox("Current Semester", options=Storage.folderpaths, index=None, placeholder="Select One")
    file = st.file_uploader("FIle To Upload", accept_multiple_files=False)

    upload = st.button("Upload", type="secondary")
    if upload:
        valid = True
        if name is None:
            st.error("Filename is required")
            valid = False
        if folder is None:
            st.error("You need to select a folder path")
            valid = False
        if file is None:
            st.error("Choose a file to upload")
            valid = False
        if not valid:
            st.error("Fix all issues then try again")
        else:
            storage = Storage()
            storage.setFile(file[0])
            storage.setName(name)
            storage.setFolderPath(folder)
            storage.saveData()
            st.success("uploaded successfully")