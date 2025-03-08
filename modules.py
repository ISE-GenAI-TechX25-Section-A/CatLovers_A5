#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)

def display_post(post_info):
    """Displays a user post in an Instagram-like style within the Streamlit app.

    Args:
        post_info (dict): The post information containing the user_id, user_image,
                          timestamp, content, and post_image.

    Returns:
        None
    """
    
    with st.container():
        col1, col2 = st.columns([1, 5]) 
        with col1:
            st.image(post_info['user_image'], width=40) 
        with col2:
            st.markdown(f"**{post_info['user_id']}**", unsafe_allow_html=True)  
            st.markdown(f"<small>{post_info['timestamp']}</small>", unsafe_allow_html=True) 

        if post_info.get('post_image'):
            st.image(post_info['post_image'], width=300) 

        st.markdown(f"<div style='font-size: 14px; margin-top: 10px;'>{post_info['content']}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # Like and Comment buttons
        col1, col2 = st.columns([1, 1]) 
        with col1:
            like_button = st.button("Like", key=f"like_{post_info['post_id']}")
            if like_button:
                st.write("You liked this post!")
        with col2:
            comment_button = st.button("Comment", key=f"comment_{post_info['post_id']}")
            if comment_button:
                st.write("Comment functionality is under development.")  # Placeholder for comment functionality



def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """
    Displays a list of recent workouts for a user in Streamlit.

    Parameters
    ----------
    workouts_list : list of dict
        Each dict should contain workout details such as:
        - 'workout_id'
        - 'start_timestamp'
        - 'end_timestamp'
        - 'distance'
        - 'steps'
        - 'calories_burned'
        - 'start_lat_lng'
        - 'end_lat_lng' 
    """
    # If no workouts, show an info message
    if not workouts_list:
        st.info("No recent workouts found.")
        return
    # Display each workout in an expander
    for workout in workouts_list:
        with st.expander(f"Workout ID: {workout['workout_id']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Start Time:** {workout['start_timestamp']}")
                st.write(f"**End Time:** {workout['end_timestamp']}")
                st.write(f"**Distance:** {workout['distance']} km")
                st.write(f"**Steps Taken:** {workout['steps']}")
                st.write(f"**Calories Burned:** {workout['calories_burned']} kcal")
                st.write(f"**Start Location (Lat, Lng):** {workout['start_lat_lng']}")
                st.write(f"**End Location (Lat, Lng):** {workout['end_lat_lng']}")


def display_genai_advice(timestamp, content, image=None):
    """Display AI-generated motivational advice with an optional image."""
    st.header("🤖 AI-Generated Advice")
    st.markdown(f"**Date:** {timestamp}")
    st.write(content)

    if image:
        st.image(image, caption="Stay motivated!", use_container_width=True)
