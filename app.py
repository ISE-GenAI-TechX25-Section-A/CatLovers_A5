#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
import os
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts, display_user_profile, display_activity_page 
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from community_page import display_community_page

from data_fetcher import (
    get_user_posts, get_genai_advice, get_user_profile, get_user_workouts
)

userId = 'user1'
Logo_path = os.path.join("Images", "Muscle Meow.png")

def display_app_page():
    """Main function to run the app."""
    st.set_page_config(page_title="Muscle Meow", page_icon="🐱💪", layout="wide")

    # Sidebar Navigation
    st.sidebar.title("🏋️ Muscle Meow Navigation")
    page = st.sidebar.radio("Go to:", ["🏠 Home","🔎 Find User", "🤖 AI Advice", "📊 Workout Summary", "📅 Recent Workouts", "📝 Posts", "👥 Community Page","🔥 Activity"])

    # Page Routing
    if page == "🏠 Home":
        # Header Section
        user_profile = get_user_profile(userId)
        st.image(Logo_path, width=100)  
        st.title(f"Welcome, {user_profile.get('full_name', 'Athlete')}! 💪🐾") #Fixed to full name because user_profile returns a dictionary with the key 'full_name'
        st.subheader("Get fit, stay pawsome! 🐱🔥")
        #display_app_page
        value = st.text_input('Enter your name')
        display_my_custom_component(value)
    elif page == "🔎 Find User":
        display_user_profile_page(userId)
    elif page == "🤖 AI Advice":
        display_ai_advice(userId)
    elif page == "📊 Workout Summary":
        display_activity_summary(get_user_workouts(userId))
    elif page == "📅 Recent Workouts":
        display_recent_workouts_page(userId)
    elif page == "📝 Posts":
        post_info = get_user_posts(userId)
        display_post(post_info)
    elif page == "👥 Community Page":
        display_community_page(userId)
    elif page == "🔥 Activity":
        display_activity_page(userId)
        

def display_ai_advice(userId):
    """Displays the AI advice page."""
    #st.header("🤖 AI Trainer: Buff Cat's Wisdom")
    advice = get_genai_advice(userId)
    display_genai_advice(advice.get("timestamp"), advice.get("content"), advice.get("image"))

    # Ask the AI (future implementation coming soon :))
    st.text_input("Ask Buff Cat a question...")

def display_recent_workouts_page(userId):
    get_user_profile(userId)
    workouts_list = get_user_workouts(userId)
    display_recent_workouts(workouts_list)

def display_user_profile_page(userId):
    user_profile = get_user_profile(userId)
    display_user_profile(user_profile)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
