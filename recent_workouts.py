# recent_workouts.py
import streamlit as st
from data_fetcher import get_user_profile, get_user_workouts
from modules import display_recent_workouts

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