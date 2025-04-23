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

#"""Displays the AI advice page."""
advice = get_genai_advice(userId)
timestamp = advice.get("timestamp")
content = advice.get("content")
image = advice.get("image")



#"""Display AI-generated motivational advice with an optional image."""
st.header("🤖 AI-Generated Advice")
st.markdown(f"**Date:** {timestamp}")
st.write(content)

if image:
    st.image(image, caption="Stay motivated!", use_container_width=True)

# Ask the AI (future implementation coming soon :))
st.text_input("Ask Buff Cat a question...")

