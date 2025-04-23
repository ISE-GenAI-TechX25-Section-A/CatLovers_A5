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
    # Sidebar Navigation
    # st.sidebar.title("🏋️ Muscle Meow Navigation")
    # page = st.sidebar.radio("Go to:", ["🏠 Home","🔎 Find User", "🤖 AI Advice", "📊 Workout Summary", "📅 Recent Workouts", "📝 Posts", "👥 Community Page","🔥 Activity"])

    # # Page Routing
    # if page == "🏠 Home":
    #     st.switch_page("pages/home_page.py")
    #     # Header Section
    #     # user_profile = get_user_profile(userId)
    #     # st.image(Logo_path, width=100)  
    #     # st.title(f"Welcome, {user_profile.get('full_name', 'Athlete')}! 💪🐾") 
    #     # st.subheader("Get fit, stay pawsome! 🐱🔥")
    #     # # value = st.text_input('Enter your name')
    #     # display_my_custom_component(value)
    # elif page == "🔎 Find User":
    #     st.switch_page("pages/user_profile_page.py")
    #     #display_user_profile_page(userId)
    # elif page == "🤖 AI Advice":
    #     st.switch_page("pages/ai_advice_page.py")
    #     #display_ai_advice(userId)
    # elif page == "📊 Workout Summary":
    #     st.switch_page("pages/workout_summary_page.py")
    #     #display_activity_summary(get_user_workouts(userId))
    # elif page == "📅 Recent Workouts":
    #     st.switch_page("pages/recent_workouts_page.py")
    #     #display_recent_workouts_page(userId)
    # elif page == "📝 Posts":
    #     st.switch_page("pages/posts_page.py")
    #     # post_info = get_user_posts(userId)
    #     # for i in range(len(post_info)):
    #     #     display_post(post_info[i], i)
    # elif page == "👥 Community Page":
    #     st.switch_page("pages/community_page.py")
    #     #display_community_page(userId)
    # elif page == "🔥 Activity":
    #     st.switch_page("pages/activity_page.py")
    #     #display_activity_page(userId)
        
        

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
    login_page()