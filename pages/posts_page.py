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
post_info = get_user_posts(userId)

    

#def display_post(post_info, key=0):
# """Displays a user post in an Instagram-like style within the Streamlit app.

# Args:
#     post_info (dict): The post information containing the user_id, user_image,
#                         timestamp, content, and post_image.

# Returns:
#     None
# """

for i in range(len(post_info)):
    with st.container():
        st.markdown('## 🤩 Your Posts')
        col1, col2 = st.columns([1, 5]) 
        with col1:
            st.image(post_info[i]['profile_image'], width=40) 
        with col2:
            st.markdown(f"**{post_info[i]['user_id']}**", unsafe_allow_html=True)  
            st.markdown(f"<small>{post_info[i]['timestamp']}</small>", unsafe_allow_html=True) 

        if post_info[i].get('image'):
            st.image(post_info[i]['image'], width=350)

        st.markdown(f"<div style='font-size: 14px; margin-top: 10px;'>{post_info[i]['content']}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # Like and Comment buttons
        col1, col2 = st.columns([1, 1]) 
        with col1:
            like_button = st.button("Like", key=f"like_{post_info[i]['post_id']}")
            if like_button:
                st.write("You liked this post!")
        with col2:
            comment_button = st.button("Comment", key=f"comment_{post_info[i]['post_id']}")
            if comment_button:
                st.write("Comment functionality is under development.")  # Placeholder for comment functionality


# if __name__ == "__main__":
#     userId = st.session_state.user_id
#     post_info = get_user_posts(userId)
#     for i in range(len(post_info)):
#         display_post(post_info[i], i)