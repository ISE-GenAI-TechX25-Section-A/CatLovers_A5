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
from datetime import datetime, timedelta
from data_fetcher import (
    get_user_posts,
    get_genai_advice,
    get_user_profile,
    get_user_sensor_data,
    get_user_workouts,
)


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
        "NAME": value,
        "BG_COLOR": "#0e1117",
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(post_info, key=0):
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
            st.image(post_info["profile_image"], width=40)
        with col2:
            st.markdown(f"**{post_info['user_id']}**", unsafe_allow_html=True)
            st.markdown(
                f"<small>{post_info['timestamp']}</small>", unsafe_allow_html=True
            )

        if post_info.get("image"):
            st.image(post_info["image"], width=350)

        st.markdown(
            f"<div style='font-size: 14px; margin-top: 10px;'>{post_info['content']}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<hr style='border: 0; border-top: 1px solid #ddd;'>",
            unsafe_allow_html=True,
        )

        # Like and Comment buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            like_button = st.button("Like", key=f"like_{post_info['post_id']}_{key}")
            if like_button:
                st.write("You liked this post!")
        with col2:
            comment_button = st.button(
                "Comment", key=f"comment_{post_info['post_id']}_{key}"
            )
            if comment_button:
                st.write(
                    "Comment functionality is under development."
                )  # Placeholder for comment functionality


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
    distances = []
    calories = []
    steps = []
    begin = []
    end = []
    # workouts_list = get_user_sensor_data("user1", "workout1")
    # st.write(workouts_list)
    # get the data from each workout in the list
    for workout in workouts_list:
        distances.append(workout["distance"])
        calories.append(workout["calories_burned"])
        steps.append(workout["steps"])
        begin.append(workout["start_timestamp"])
        end.append(workout["end_timestamp"])

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

    days_of_week = {
        "Monday": monday,
        "Tuesday": tuesday,
        "Wednesday": wednesday,
        "Thursday": thursday,
        "Friday": friday,
        "Saturday": saturday,
        "Sunday": sunday,
    }
    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]  # Line written by ChatGPT
    time_of_day = {"Morning": morning, "Afternoon": afternoon, "Evening": evening}

    # splits the timestamp data into date and time and uses the hour to determine the time of day and the date to determine day of the week
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
        days_of_week[day_names[weekday]] += 1  # Line written by ChatGPT

    # workout length calculation written by ChatGPT
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

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Recent Workouts")
        if st.button("See More"):
            # page = "📅 Recent Workouts"
            st.write("Functionality Currently Under Development")
            # pass
            # st.switch_page("/CatLovers_A5/[page_name].py")

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

    # st.caption(f"Congratulations! Your favorite time to workout is {fav_time_of_day}. You work out most on {fav_day_of_week}. You burn an average of {avg_calories} calories in {workoutLength} time.")
    st.markdown(
        f"""
    <div style="text-align: center; font-size: 0.8em;">
        Congratulations! Your favorite time to workout is <b>{fav_time_of_day}</b>.
        You work out most on <b>{fav_day_of_week}</b>. You burn an average of <b>{avg_calories}</b> calories in <b>{workoutLength}</b> time.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.bar_chart(days_of_week, x_label="Weekday", y_label="Frequency")


def display_recent_workouts(workouts_list):
    # Page header
    st.markdown(
        "<h1 style='text-align: center; color: orange;'>🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: gray;'>Train like a beast, rest like a cat. 😼</h3>",
        unsafe_allow_html=True,
    )

    # Get user input for user ID
    user_id = st.text_input("🔍 Enter user ID", "user1")
    if not user_id:
        st.warning("⚠️ Please enter a valid user ID.")
        return
    if user_id != "user1":
        workouts = get_user_workouts(user_id)
    else:
        workouts = workouts_list

    # Button to trigger the workouts display
    if st.button("🐾Show Recent Workouts🐾"):
        try:
            st.subheader(f"{user_id}'s Recent Workouts Overview")

            # If there are workouts, display each one in an expander.
            if workouts:
                for workout in workouts:
                    with st.expander(f"Workout ID: {workout['workout_id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Start Time:** {workout['start_timestamp']}")
                            st.write(f"**End Time:** {workout['end_timestamp']}")
                            st.write(f"**Distance:** {workout['distance']} km")
                            st.write(f"**Steps Taken:** {workout['steps']}")
                            st.write(
                                f"**Calories Burned:** {workout['calories_burned']} kcal"
                            )
                            st.write(
                                f"**Start Location (Lat, Lng):** ({workout['start_lat_lng']['lat']},{workout['start_lat_lng']['lng']})"
                            )
                            st.write(
                                f"**End Location (Lat, Lng):** ({workout['end_lat_lng']['lat']},{workout['end_lat_lng']['lng']})"
                            )
                st.divider()
                st.markdown(
                    "<h3 style='text-align: center; color: green;'>🔥 Push yourself! No one is going to do it for you! 🔥</h3>",
                    unsafe_allow_html=True,
                )
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


def display_user_profile(user_profile):
    # Page header
    st.markdown(
        "<h1 style='text-align: center; color: orange;'>😺💼 Muscle Meow: User Profile 📋</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: gray;'>Every legend starts with a profile. 🔍</h3>",
        unsafe_allow_html=True,
    )

    # Input box to type a User ID
    user_id = st.text_input("🆔 Enter user ID", "user1")
    if not user_id:
        st.warning("⚠️ Please enter a valid user ID.")
        return

    if st.button("📂 Show User Profile"):
        try:
            # Retrieve user profile
            if user_id != "user1":
                user = get_user_profile(user_id)
            else:
                user = user_profile

            # Display user information
            if user_id == "user1" or user_id == "user2" or user_id == "user3":
                st.subheader(f"👤 Profile: {user['full_name']} (@{user['username']})")

                col1, col2 = st.columns([1, 2])
                with col1:
                    # st.write(user['profile_image'])
                    st.image(
                        user["profile_image"], caption="Profile Picture", width=250
                    )
                with col2:
                    st.write(f"**Full Name:** {user['full_name']}")
                    st.write(f"**Username:** {user['username']}")
                    st.write(f"**Date of Birth:** {user['date_of_birth']}")
                    st.write(f"**User ID:** {user_id}")
                    st.write(f"**Number of Friends:** {len(user['friends'])}")

                # Display friends list
                if user["friends"]:
                    st.markdown("---")
                    st.markdown("### 🧑‍🤝‍🧑 Friends")
                    for friend_id in user["friends"]:
                        st.write(f"• {friend_id}")
                else:
                    st.info("This user has no friends 😿")
            else:
                st.info("No user profile found.")

        except ValueError:
            st.error(f"'{user_id}' was not found.")


def display_activity_page(user_id):
    """Displays the user's activity page with recent workouts, a summary, and a share button."""
    st.markdown("## 🔥 Your Activity")

    # Fetch workouts
    workouts = get_user_workouts(user_id)
    if not workouts:
        st.warning("No workouts found.")
        return

    # Display Recent 3 Workouts
    st.markdown("### 🏃 Recent Workouts")
    recent_workouts = sorted(
        workouts, key=lambda w: w["start_timestamp"], reverse=True
    )[:3]
    for workout in recent_workouts:
        with st.expander(f"Workout: {workout['start_timestamp']}"):
            st.write(f"Distance: {workout['distance']} km")
            st.write(f"Steps: {workout['steps']}")
            st.write(f"Calories Burned: {workout['calories_burned']}")

    # Display Activity Summary
    st.markdown("---")
    st.markdown("### 📊 Activity Summary")
    display_activity_summary(workouts)

    # Share a Stat
    st.markdown("---")
    st.markdown("### ✨ Share Your Stats")
    stat_option = st.selectbox(
        "Pick a stat to share with your friends:", ["Steps", "Calories", "Distance"]
    )
    stat_map = {
        "Steps": lambda w: w["steps"],
        "Calories": lambda w: w["calories_burned"],
        "Distance": lambda w: w["distance"],
    }
    selected_workout = recent_workouts[0] if recent_workouts else None
    if selected_workout and st.button("Share it!"):
        value = stat_map[stat_option](selected_workout)
        content = f"Look at this, I logged {value} {stat_option.lower()} today! 💪🐾"
        st.success("Post shared with the community!")

        post = {
            "user_id": get_user_profile(user_id)["username"],
            "post_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "content": content,
            "user_image": get_user_profile(user_id)["profile_image"],
            "post_image": "https://i.imgur.com/61ZEkcrb.jpg",
        }
        display_post(post)


# ACCOUNTABILITY TRACKER
def display_streak_tracker(user_id):
    workouts_list = get_user_workouts(user_id)
    weekdays = [workout["start_timestamp"].date() for workout in workouts_list]
    weekdays.sort()

    streak = 1 if weekdays else 0
    for i in range(1, len(weekdays)):
        if weekdays[i] == weekdays[i - 1] + timedelta(days=1):
            streak += 1
        else:
            streak = 1

    if streak == 7:
        congrats = "Good job on making it one week without missing a day! You've earned 5 Buff Cat Points!"
    elif streak == 30:
        congrats = "Proud of you for making it 30 days without missing a day! You've earned 15 Buff Cat Points!"
    elif streak == 180:
        congrats = "You're so awesome for making it 180 days without missing a day! You've earned 30 Buff Cat Points!"
    elif streak == 365:
        congrats = "Wow, you made it one year without missing a day! You've earned 50 Buff Cat Points!"
    else:
        congrats = ""

    st.markdown(
        f"""
    <div style=\"text-align: center; font-size: 1.2em; margin-top: 20px;\">
        <strong>🔥 Streak Tracker:</strong><br>
        {streak} days<br>
        <em>{congrats}</em>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_goal_progress_bars(user_id):
    daily_progress = 0.66
    weekly_progress = 0.30
    monthly_progress = 0.10

    st.markdown("### 🎯 Goal Progress")

    st.progress(daily_progress, text="Daily Progress")
    st.progress(weekly_progress, text="Weekly Progress")
    st.progress(monthly_progress, text="Monthly Progress")


def display_buff_cat_points(user_id):
    points = 120
    st.markdown("### 💪 Buff Cat Points")
    st.markdown(
        f"<div style='font-size: 28px; color: orange;'>⭐ {points} Points</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "\nBuff Cat Points are your reward system! You earn between 5 and 15 points for every workout you log, depending on difficulty.\nTrack your points to stay motivated and unlock milestones!"
    )


def display_goal_creation_ui():
    st.markdown("### 🛠️ Create New Fitness Goals")

    goal_tabs = st.tabs(["📆 Daily", "📈 Weekly", "📊 Monthly"])

    goal_data = st.session_state.setdefault(
        "goal_data", {"Daily": [], "Weekly": [], "Monthly": []}
    )

    for i, timeframe in enumerate(["Daily", "Weekly", "Monthly"]):
        with goal_tabs[i]:
            left, right = st.columns([1, 1])
            with left:
                new_goal = st.text_input(
                    f"Enter a {timeframe} Goal", key=f"{timeframe}_goal_input"
                )
                if st.button(f"➕ Add {timeframe} Goal"):
                    if new_goal:
                        goal_data[timeframe].append(
                            {"text": new_goal, "completed": False}
                        )
                        st.success(f"Added {timeframe.lower()} goal: {new_goal}")

                st.markdown("### 🏋️ Track Preloaded Workouts")
                muscle_group = st.selectbox(
                    "Select Muscle Group",
                    ["Legs", "Upper Body", "Core"],
                    key=f"group_{timeframe}",
                )
                if muscle_group == "Legs":
                    workouts = ["Squats", "Leg Press", "Lunges"]
                elif muscle_group == "Upper Body":
                    workouts = ["Push-Ups", "Pull-Ups", "Bench Press"]
                elif muscle_group == "Core":
                    workouts = ["Crunches", "Plank", "Russian Twist"]
                else:
                    workouts = []
                selected_workout = st.selectbox(
                    "Pick a Workout", workouts, key=f"workout_{timeframe}"
                )
                if st.button("➕ Add Work", key=f"log_{timeframe}"):
                    goal_data[timeframe].append(
                        {"text": selected_workout, "completed": False}
                    )
                    st.success(f"Added: {selected_workout}")

            with right:
                if goal_data[timeframe]:
                    st.markdown(f"### {timeframe} Goals:")
                    for idx, goal in enumerate(goal_data[timeframe]):
                        col1, col2 = st.columns([0.9, 0.1])
                        with col1:
                            status = "✅" if goal["completed"] else "⬜"
                            st.write(f"{status} {goal['text']}")
                        with col2:
                            if not goal["completed"]:
                                if st.button("✔️", key=f"check_{timeframe}_{idx}"):
                                    goal["completed"] = True


def display_preloaded_workout_logger():
    pass  # moved inside display_goal_creation_ui
