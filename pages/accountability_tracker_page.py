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

# # if no workouts, streak is 0
# streak = 1 if weekdays else 0  

# for i in range(1, len(weekdays)):
#     # Check if current date is exactly 1 day after previous
#     if weekdays[i] == weekdays[i - 1] + timedelta(days=1):
#         streak += 1
#     else:
#         streak = 1  # reset if break in streak
# #TODO: give the users actual buff cat points once that system is in place
# if streak == 7:
#     congrats = "Good job on making it one week without missing a day! You've earned 5 buff cat points!"
# elif streak == 30:
#     congrats = "Proud of you for making it 30 days without missing a day! You've earned 15 buff cat points!"
# elif streak == 180:
#     congrats = "You're so awesome for making it 180 days without missing a day! You've earned 30 buff cat points!"
# elif streak == 365:
#     congrats = "Wow, I'm so happy you made it one year without missing a day! You've earned 50 buff cat points!"
# else:
#     congrats = ""
# st.markdown(
# f"""
# <div style="text-align: center; font-size: 1em;">
# Streak Tracker\n
# {streak}\n
# {congrats}
# </div>
# """,
# unsafe_allow_html=True
# )

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
