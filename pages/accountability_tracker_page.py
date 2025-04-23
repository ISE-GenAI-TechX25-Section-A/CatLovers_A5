import streamlit as st
import os
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from internals import create_component
import statistics
import calendar
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
from modules import display_goal_creation_ui

userId = st.session_state.get("user_id", None)
# Redirect trigger from workout page
if st.session_state.get("redirect_to_accountability", False):
    st.session_state.redirect_to_accountability = False
    st.rerun()

workouts_list = get_user_workouts(userId)

col1, col2 = st.columns([1,1])

with col1:
    st.title("✅ Workouts Completed")

with col2:
    st.title("📝 Goals")


#getting days workouted on
weekdays = []
for workout in workouts_list:
    weekdays.append(workout['start_timestamp'].date())

weekdays.sort()

from modules import (
    display_streak_tracker,
    display_goal_progress_bars,
    display_buff_cat_points,
    display_goal_creation_ui,
    display_preloaded_workout_logger
)

# visuals
display_streak_tracker(userId)
display_goal_progress_bars(userId)
display_buff_cat_points(userId)
display_goal_creation_ui()
if st.button("Create Daily Workout Plan"):
    st.switch_page("pages/add_workout_page.py")
    
display_preloaded_workout_logger()
