#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import statistics
import calendar
import streamlit as st
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta





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
            st.image(post_info['post_image'], width=350) 

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
    """
    Calculates the averages per workout of the workout characteristics
    Displays a summary of the averages
    Links to the "recent workouts" page

    Parameters: 
        workouts_list: a list of workouts for a specified user
            workouts contain: 
                'workout_id'
                'start_timestamp'
                'end_timestamp'
                'start_lat_lng'
                'end_lat_lng'
                'distance'
                'steps'
                'calories_burned'

    Returns: 
        Nothing
    
    """
    #get the data from each workout in the list
    for workout in workouts_list:
        distances = [workout['distance']]
        calories = [workout['calories_burned']]
        steps = [workout['steps']]
        begin = [workout['start_timestamp']]
        end = [workout['end_timestamp']]
    
    avg_distances = statistics.mean(distances)
    avg_calories = statistics.mean(calories)
    avg_steps = statistics.mean(steps)

    morning = 0
    afternoon = 0
    evening = 0

    monday = 0
    tuesday = 0
    wednesday = 0
    thursday = 0
    friday = 0
    saturday = 0
    sunday = 0

    days_of_week = {"Monday":monday, "Tuesday":tuesday, "Wednesday":wednesday, "Thursday":thursday, "Friday":friday, "Saturday":saturday, "Sunday":sunday}
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] #Line written by ChatGPT
    time_of_day = {"Morning":morning, "Afternoon":afternoon, "Evening":evening}


    #splits the timestamp data into date and time and uses the hour to determine the time of day and the date to determine day of the week
    for timestamp in begin:
        date, time = timestamp.split(' ')
        hour, minute, second = time.split(':')
        year, month, day = date.split("-")
        
        hour = int(hour)
        if hour < 12:
            time_of_day["Morning"] += 1
        elif hour > 17:
            time_of_day["Evening"] += 1
        else:
            time_of_day["Afternoon"] += 1
        
        weekday = calendar.weekday(int(year), int(month), int(day))
        days_of_week[day_names[weekday]] += 1 #Line written by ChatGPT

    
    #workout length calculation written by ChatGPT
    lengths = []
    for i in range(len(begin)):
        start_time = datetime.strptime(begin[i], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end[i], "%Y-%m-%d %H:%M:%S")
        
        lengths.append((end_time - start_time).total_seconds())
    
    avg_seconds = statistics.mean(lengths)
    avg_duration = timedelta(seconds=avg_seconds)
    hours, remainder = divmod(avg_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    workoutLength = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    fav_time_of_day = max(time_of_day, key=time_of_day.get)
    fav_day_of_week = max(days_of_week, key=days_of_week.get)



    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader("Recent Workouts")
        if st.button("See More"):
            #page = "📅 Recent Workouts"
            st.write("Functionality Currently Under Development")
            #pass
            #st.switch_page("/CatLovers_A5/[page_name].py")

    with col2:
        st.subheader("Summary")

        subcol1, subcol2 = st.columns(2)

        with subcol1:
            st.metric("Average Calories Burned", avg_calories)
            st.metric("Average Distance Travelled", avg_distances)
            st.metric("Average Steps Taken", avg_steps)
        with subcol2:
            st.metric("Favorite Time of Day", fav_time_of_day)
            st.metric("Favorite Day of Week", fav_day_of_week)
            st.metric("Average Length of Workouts", workoutLength)

    #st.caption(f"Congratulations! Your favorite time to workout is {fav_time_of_day}. You work out most on {fav_day_of_week}. You burn an average of {avg_calories} calories in {workoutLength} time.")
    st.markdown(
    f"""
    <div style="text-align: center; font-size: 0.8em;">
        Congratulations! Your favorite time to workout is <b>{fav_time_of_day}</b>.
        You work out most on <b>{fav_day_of_week}</b>. You burn an average of <b>{avg_calories}</b> calories in <b>{workoutLength}</b> time.
    </div>
    """,
    unsafe_allow_html=True
)

    st.bar_chart(days_of_week, x_label="Weekday", y_label="Frequency")

    
    


def display_recent_workouts(workouts_list):
    # Page header
    st.markdown("<h1 style='text-align: center; color: orange;'>🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Train like a beast, rest like a cat. 😼</h3>", unsafe_allow_html=True)
    
    # Get user input for user ID
    user_id = st.text_input("🔍 Enter user ID", "user1")
    if not user_id:
        st.warning("⚠️ Please enter a valid user ID.")
        return

    # Button to trigger the workouts display
    if st.button("🐾Show Recent Workouts🐾"):
        try:
            st.subheader(f"{user_id}'s Recent Workouts Overview")

            # If there are workouts, display each one in an expander.
            if workouts_list:
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
                st.divider()
                st.markdown("<h3 style='text-align: center; color: green;'>🔥 Push yourself! No one is going to do it for you! 🔥</h3>", unsafe_allow_html=True)
            else:
                st.info("No recent workouts found.")
        except ValueError:
            st.error(f"User '{user_id}' not found. Please try again.")


def display_genai_advice(timestamp, content, image=None):
    """Display AI-generated motivational advice with an optional image."""
    st.header("🤖 AI-Generated Advice")
    st.markdown(f"**Date:** {timestamp}")
    st.write(content)

    if image:
        st.image(image, caption="Stay motivated!", use_container_width=True)
