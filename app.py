#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
# If 'TypeError: string indices must be integers, not 'str'':
#    gcloud config set project brianrivera26techx25
#    gcloud config set account 732301616375-compute@developer.gserviceaccount.com
#    gcloud auth application-default login

#############################################################################

import streamlit as st
import os
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts, display_user_profile, display_activity_page, display_exercise_card
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

from data_fetcher import (
    get_user_posts, get_genai_advice, get_user_profile, get_user_workouts
)

st.set_page_config(page_title="Muscle Meow", page_icon="🐱💪", layout="wide")
def login_page():
    """Displays the login page."""
    if "user_id" not in st.session_state:
        # Hide sidebar when not logged in using css 
        hide_sidebar_and_icon = """
            <style>
                /* Hide entire sidebar */
                [data-testid="stSidebar"] {
                    display: none !important;
                }

                /* Hide the top-left sidebar toggle button */
                [data-testid="collapsedControl"] {
                    display: none !important;
                }
            </style>
        """
        st.markdown(hide_sidebar_and_icon, unsafe_allow_html=True)

        st.title("Login to Muscle Meow🐱💪")
        user_id = st.text_input("🆔 Enter your user ID:")

        if st.button("Login"):
            if user_id:
                st.session_state.user_id = user_id  # Store user ID in session state
                st.success(f"Logged in as {user_id}")
                st.rerun()
            else:
                st.error("Please enter a valid user ID.")
    else:
        # Redirect to main content if already logged in
        display_app_page()


Logo_path = os.path.join("Images", "Muscle Meow.png")

def display_app_page():
    userId = st.session_state.user_id
    pages = {
        "Your account": [
            st.Page("pages/home_page.py", title="🏠 Home"),
            st.Page("pages/posts_page.py", title="📝 Posts"),
            st.Page("pages/ai_advice_page.py", title="🤖 AI Advice"),
            st.Page("pages/accountability_tracker_page.py", title="🧐 Accountability Tracker"),
        ],
        "Your Workouts": [
            st.Page("pages/workout_summary_page.py", title="📊 Workout Summary"),
            st.Page("pages/recent_workouts_page.py", title="📅 Recent Workouts"),
            st.Page("pages/activity_page.py", title="🔥 Activity"),
            st.Page("pages/add_workout_page.py", title="🔥 Exercises"),
        ],
        "Friends":[
            st.Page("pages/user_profile_page.py", title="🔎 Find User"),
            st.Page("pages/community_page.py", title="👥 Community Page"),
        ]
    }

    page = st.navigation(pages)
    page.run()

    #spacing before logout button
    with st.sidebar:
        #st.markdown("<br><hr><br>", unsafe_allow_html=True)
        # Log Out Button
        if st.button("🚪 Log Out"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    login_page()