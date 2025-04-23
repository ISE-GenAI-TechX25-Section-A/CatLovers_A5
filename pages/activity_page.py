import streamlit as st
import os
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from internals import create_component
import statistics
import calendar
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from modules import display_post
from datetime import datetime, timedelta
import uuid

#"""Displays the user's activity page with recent workouts, a summary, and a share button."""
userId = st.session_state.get("user_id", None)
# Fetch workouts
workouts = get_user_workouts(userId)
user_id = userId
st.markdown("## 🔥 Your Activity")


# Display Recent 3 Workouts
st.markdown("### 🏃 Recent Workouts")
recent_workouts = sorted(workouts, key=lambda w: w['start_timestamp'], reverse=True)[:3]
for workout in recent_workouts:
    with st.expander(f"Workout: {workout['start_timestamp']}"):
        st.write(f"Distance: {workout['distance']} km")
        st.write(f"Steps: {workout['steps']}")
        st.write(f"Calories Burned: {workout['calories_burned']}")

# Display Activity Summary
st.markdown("---")
st.markdown("### 📊 Activity Summary")
distances = []
calories = []
steps = []
begin = []
end = []
#get the data from each workout in the list
for workout in workouts:
    distances.append(workout['distance'])
    calories.append(workout['calories_burned'])
    steps.append(workout['steps'])
    begin.append(workout['start_timestamp'])
    end.append(workout['end_timestamp'])

avg_distances = round(statistics.mean(distances), 2)
avg_calories = round(statistics.mean(calories), 2)
avg_steps = round(statistics.mean(steps), 2)

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
    date = timestamp.date()
    time = timestamp.time()
    hour = timestamp.hour
    minute = timestamp.minute
    second = timestamp.second
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    
    if hour < 12:
        time_of_day["Morning"] += 1
    elif hour > 17:
        time_of_day["Evening"] += 1
    else:
        time_of_day["Afternoon"] += 1
    
    weekday = calendar.weekday(year, month, day)
    days_of_week[day_names[weekday]] += 1 #Line written by ChatGPT


#workout length calculation written by ChatGPT
lengths = []
for i in range(len(begin)):
    start_time = begin[i]
    end_time = end[i]
    
    lengths.append((end_time - start_time).total_seconds())

avg_seconds = statistics.mean(lengths)
avg_duration = timedelta(seconds=avg_seconds)
hours, remainder = divmod(avg_duration.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

workoutLength = f"{hours:02}:{minutes:02}:{seconds:02}"

fav_time_of_day = max(time_of_day, key=time_of_day.get)
fav_day_of_week = max(days_of_week, key=days_of_week.get)


subcol1, subcol2 = st.columns(2)

with subcol1:
    st.metric("Average Calories Burned", avg_calories)
    st.metric("Average Distance Travelled", avg_distances)
    st.metric("Average Steps Taken", avg_steps)
with subcol2:
    st.metric("Favorite Time of Day", fav_time_of_day)
    st.metric("Favorite Day of Week", fav_day_of_week)
    st.metric("Average Length of Workouts", workoutLength)

# Share a Stat
st.markdown("---")
st.markdown("### ✨ Share Your Stats")
stat_option = st.selectbox("Pick a stat to share with your friends:", ["Steps", "Calories", "Distance"])
stat_map = {
    "Steps": lambda w: w['steps'],
    "Calories": lambda w: w['calories_burned'],
    "Distance": lambda w: w['distance']
}
selected_workout = recent_workouts[0] if recent_workouts else None
if selected_workout and st.button("Share it!"):
    value = stat_map[stat_option](selected_workout)
    content = f"Look at this, I logged {value} {stat_option.lower()} today! 💪🐾"
    st.success("Post shared with the community!")

    # You can replace this with actual BigQuery insertion later
    post = {
        'user_id': get_user_profile(user_id)['username'],
        'post_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'content': content,
        'user_image': get_user_profile(user_id)['profile_image'],
        'post_image': 'https://i.imgur.com/61ZEkcrb.jpg'
    }
    display_post(post)

