from internals import create_component
import statistics
import calendar
import streamlit as st
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = st.session_state.get("user_id", None)

get_user_profile(userId)
workouts_list = get_user_workouts(userId)

# Page header
st.markdown("<h1 style='text-align: center; color: orange;'>🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Train like a beast, rest like a cat. 😼</h3>", unsafe_allow_html=True)

# Get user input for user ID
user_id = st.text_input("🔍 Enter user ID", "user1")
if not user_id:
    st.warning("⚠️ Please enter a valid user ID.")
if user_id != 'user1':
    workouts = get_user_workouts(user_id)
else:
    workouts = workouts_list

# Button to trigger the workouts display
if st.button("🐾Show Recent Workouts🐾"):
    try:
        st.subheader(f"{user_id}'s Recent Workouts Overview")

        # If there are workouts, display each one in an expander.
        if workouts:
            for workout in workouts:
                with st.expander(f"Workout ID: {workout['workout_id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Start Time:** {workout['start_timestamp']}")
                        st.write(f"**End Time:** {workout['end_timestamp']}")
                        st.write(f"**Distance:** {workout['distance']} km")
                        st.write(f"**Steps Taken:** {workout['steps']}")
                        st.write(f"**Calories Burned:** {workout['calories_burned']} kcal")
                        st.write(f"**Start Location (Lat, Lng):** ({workout['start_lat_lng']['lat']},{workout['start_lat_lng']['lng']})")
                        st.write(f"**End Location (Lat, Lng):** ({workout['end_lat_lng']['lat']},{workout['end_lat_lng']['lng']})")
            st.divider()
            st.markdown("<h3 style='text-align: center; color: green;'>🔥 Push yourself! No one is going to do it for you! 🔥</h3>", unsafe_allow_html=True)
        else:
            st.info("No recent workouts found.")
    except ValueError:
        st.error(f"User '{user_id}' not found. Please try again.")

