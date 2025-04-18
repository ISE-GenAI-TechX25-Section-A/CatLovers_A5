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

userId = st.session_state.get("user_id", None)

#def display_user_profile_page(userId):
user_profile = get_user_profile(userId)
    #display_user_profile(user_profile)

#def display_user_profile(user_profile):
# Page header
st.markdown("<h1 style='text-align: center; color: orange;'>😺💼 Muscle Meow: User Profile 📋</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Every legend starts with a profile. 🔍</h3>", unsafe_allow_html=True)

# Input box to type a User ID
user_id = st.text_input("🆔 Enter user ID", "user1")
if not user_id:
    st.warning("⚠️ Please enter a valid user ID.")
    #return

if st.button("📂 Show User Profile"):
    try:
        # Retrieve user profile
        if user_id != 'user1':
            user = get_user_profile(user_id)
        else:
            user = user_profile

        # Display user information
        if user_id == 'user1' or user_id == 'user2' or user_id == 'user3':
            st.subheader(f"👤 Profile: {user['full_name']} (@{user['username']})")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                # st.write(user['profile_image'])
                st.image(user['profile_image'], caption="Profile Picture", width=250)
            with col2:
                st.write(f"**Full Name:** {user['full_name']}")
                st.write(f"**Username:** {user['username']}")
                st.write(f"**Date of Birth:** {user['date_of_birth']}")
                st.write(f"**User ID:** {user_id}")
                st.write(f"**Number of Friends:** {len(user['friends'])}")

            # Display friends list
            if user['friends']:
                st.markdown("---")
                st.markdown("### 🧑‍🤝‍🧑 Friends")
                for friend_id in user['friends']:
                    st.write(f"• {friend_id}")
            else:
                st.info("This user has no friends 😿")
        else:
            st.info("No user profile found.")

    except ValueError:
        st.error(f"'{user_id}' was not found.")

# if __name__ == "__main__":
#     userId = st.session_state.user_id
#     display_user_profile_page(userId)