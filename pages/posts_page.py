from internals import create_component
import statistics
import calendar
import streamlit as st
from streamlit_elements import elements, mui, html
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = st.session_state.get("user_id", None)
post_info = get_user_posts(userId)


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
            post_id = post_info[i]['post_id']
            comment_key = f"comment_text_{post_id}"
            show_comment_box_key = f"show_comment_box_{post_id}"

            # Show comment box when button is clicked
            if st.button("Comment", key=f"comment_button_{post_id}"):
                st.session_state[show_comment_box_key] = True

            # Show the text input and done button if toggled on
            if st.session_state.get(show_comment_box_key, False):
                comment = st.text_input("Write your comment", key=comment_key)
                if st.button("Done", key=f"done_button_{post_id}"):
                    if comment:
                        st.success(f"Added your comment!")
                        st.write(f"Comment by {userId}: \n {comment}")
                    else:
                        st.warning("Comment can't be empty.")
                    # Reset state to hide input after done
                    st.session_state[show_comment_box_key] = False
                    time.sleep(1)
                    st.rerun()