#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
import os
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

from data_fetcher import (
    get_user_posts, get_genai_advice, get_user_profile, get_user_workouts
)

userId = 'user1'
Logo_path = os.path.join("Images", "Muscle Meow.png")

def display_app_page():
    """Main function to run the app."""
    st.set_page_config(page_title="Muscle Meow", page_icon="🐱💪", layout="wide")

    # Header Section
    user_profile = get_user_profile(userId)
    st.image(Logo_path, width=100)  
    st.title(f"Welcome, {user_profile.get('name', 'Athlete')}! 💪🐾")
    st.subheader("Get fit, stay pawsome! 🐱🔥")

    # Sidebar Navigation
    st.sidebar.title("🏋️ Muscle Meow Navigation")
    page = st.sidebar.radio("Go to:", ["🏠 Home", "🤖 AI Advice", "📊 Workout Summary", "📅 Recent Workouts", "📝 Posts"])

    # Page Routing
    if page == "🏠 Home":
        display_app_page
    elif page == "🤖 AI Advice":
        display_ai_advice(userId)
    elif page == "📊 Workout Summary":
        display_activity_summary(get_user_workouts(userId))
    elif page == "📅 Recent Workouts":
        display_recent_workouts(get_user_workouts(userId))
    elif page == "📝 Posts":
        display_post(userId)


def display_ai_advice(userId):
    """Displays the AI advice page."""
    #st.header("🤖 AI Trainer: Buff Cat's Wisdom")
    advice = get_genai_advice(userId)
    display_genai_advice(advice.get("timestamp"), advice.get("content"), advice.get("image"))

    # Ask the AI (future implementation coming soon :))
    st.text_input("Ask Buff Cat a question...")

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
