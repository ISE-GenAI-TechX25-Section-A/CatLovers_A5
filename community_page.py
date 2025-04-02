import streamlit as st
import os
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile

"""
Create a community_page.py file. This page is a “home” page for socialization across the app. It must include:
First 10 posts from a user’s friends ordered by timestamp
One piece of GenAI advice and encouragement

"""
#Example Data:

#A single dictionary with the keys full_name, username, date_of_birth, profile_image, and friends (containing a list of friend user_ids)
profile = {"full_name": "Alice Johnson", "username": "alicej", "date_of_birth": "1990-01-15", "profile_image": "http://example.com/images/alice.jpg",
"friends": ["user2", "user3"]}

#A list of posts. Each post is a dictionary with keys user_id, post_id, timestamp, content, and image.
posts = [
    []
]

def display_community_page(userId):
    profile = {}
    profile = get_user_profile(userId) #dictionary. One of the keys is a list of friend userIds
    posts = [] #a list filled with a list of dictionaries of posts
    friends = profile["friends"] #a list of friend userIds
    for user in friends:
        posts.append(get_user_posts(user))

