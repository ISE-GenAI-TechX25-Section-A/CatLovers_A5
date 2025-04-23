from internals import create_component
import statistics
import calendar
import streamlit as st
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = st.session_state.get("user_id", None)
workouts_list = get_user_workouts(userId)


distances = []
calories = []
steps = []
begin = []
end = []

#get the data from each workout in the list
for workout in workouts_list:
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



col1, col2 = st.columns([1,2])

with col1:
    st.markdown("### 🏃 Recent Workouts")
    if st.button("See More"):
        st.switch_page("pages/recent_workouts_page.py")

with col2:
    st.markdown("### 📊 Activity Summary")

    subcol1, subcol2 = st.columns(2)

    with subcol1:
        st.metric("Average Calories Burned", avg_calories)
        st.metric("Average Distance Travelled", avg_distances)
        st.metric("Average Steps Taken", avg_steps)
    with subcol2:
        st.metric("Favorite Time of Day", fav_time_of_day)
        st.metric("Favorite Day of Week", fav_day_of_week)
        st.metric("Average Length of Workouts", workoutLength)

st.markdown('### ✨ Stats')
st.markdown(
f"""
<div style="text-align: center; font-size: 1em;">
    Congratulations! Your favorite time to workout is <b>{fav_time_of_day}</b>.
    You work out most on <b>{fav_day_of_week}</b>. You burn an average of <b>{avg_calories}</b> calories in <b>{workoutLength}</b> time.
</div>
""",
unsafe_allow_html=True
)

st.bar_chart(days_of_week, x_label="Weekday", y_label="Frequency")
