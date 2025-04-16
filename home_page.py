import streamlit as st
import os
from modules import display_my_custom_component

def main():
    # Header Section
    user_profile = get_user_profile(userId)
    st.image(Logo_path, width=100)  
    st.title(f"Welcome, {user_profile.get('name', 'Athlete')}! 💪🐾")
    st.subheader("Get fit, stay pawsome! 🐱🔥")
    value = st.text_input('Enter your name')
    display_my_custom_component(value)

if __name__ == "__main__":
    main()