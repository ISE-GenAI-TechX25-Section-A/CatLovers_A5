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


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    pass


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
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


    #split the timestamps to date and time
    #check for the time in the "morning" and add one to morning
    # check which one has the highest count and that will be favorite time of day
    for timestamp in begin:
        date, time = timestamp.split(' ')
        hour, minute, second = time.split(':')
        year, month, day = date.split("-")
        
        hour = int(hour)
        if hour < 12:
            morning += 1
        elif hour > 17:
            evening += 1
        else:
            afternoon += 1
        
        weekday = calendar.weekday(int(year), int(month), int(day))
        if weekday == 0:
            monday += 1
        elif weekday == 1:
            tuesday += 1
        elif weekday == 2:
            wednesday += 1
        elif weekday == 3:
            thursday += 1
        elif weekday == 4:
            friday += 1
        elif weekday == 5:
            saturday += 1
        elif weekday == 6:
            sunday += 1

    
    fav_time_of_day = max(morning, afternoon, evening)
    fav_day_of_week = max(monday, tuesday, wednesday, thursday, friday, saturday, sunday)

    
    #use a calendar function to see what day of the week the date is on
    #add count to that week
    # day with highest count is favorite day of week. If equal, choose a random one

    st.header("Hello, [user]!")
    


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
