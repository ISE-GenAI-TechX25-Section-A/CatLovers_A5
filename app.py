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
        # Header Section
        user_profile = get_user_profile(userId)
        st.image(Logo_path, width=100)  
        st.title(f"Welcome, {user_profile.get('name', 'Athlete')}! 💪🐾")
        st.subheader("Get fit, stay pawsome! 🐱🔥")
        #display_app_page
        value = st.text_input('Enter your name')
        display_my_custom_component(value)
    elif page == "🤖 AI Advice":
        display_ai_advice(userId)
    elif page == "📊 Workout Summary":
        display_activity_summary(get_user_workouts(userId))
    elif page == "📅 Recent Workouts":
        display_recent_workouts_page()
    elif page == "📝 Posts":
        post_info = get_user_posts(userId)
        display_post(post_info)

def display_ai_advice(userId):
    """Displays the AI advice page."""
    #st.header("🤖 AI Trainer: Buff Cat's Wisdom")
    advice = get_genai_advice(userId)
    display_genai_advice(advice.get("timestamp"), advice.get("content"), advice.get("image"))

    # Ask the AI (future implementation coming soon :))
    st.text_input("Ask Buff Cat a question...")

def display_recent_workouts_page():
    """Displays recent workouts for a user."""
    st.markdown("<h1 style='text-align: center; color: orange;'>🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Train like a beast, rest like a cat. 😼</h3>", unsafe_allow_html=True)

    user_id = st.text_input("🔍 Enter user ID", "user1")
    if not user_id:
        st.warning("⚠️ Please enter a valid user ID.")
        return

    # Button to trigger the display of recent workouts
    if st.button("🐾Show Recent Workouts🐾"):
        try:
            st.subheader(f"{user_id}'s Recent Workouts Overview")
            # This will raise ValueError if the user doesn't exist
            get_user_profile(user_id)

            # Fetch the user's workouts
            workouts_list = get_user_workouts(user_id)

            # Display them using your function from modules.py
            display_recent_workouts(workouts_list)

            if workouts_list:  
                st.divider()
                st.markdown("<h3 style='text-align: center; color: green;'>🔥 Push yourself! No one is going to do it for you! 🔥</h3>", unsafe_allow_html=True)

        except ValueError:
            # If user not found, show an error
            st.error(f"User '{user_id}' not found. Please try again.")

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
