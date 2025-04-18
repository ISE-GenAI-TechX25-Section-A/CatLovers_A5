import streamlit as st
import os
from internals import create_component
import streamlit.components.v1 as components
#from modules import display_my_custom_component
from data_fetcher import get_user_profile

Logo_path = os.path.join("Images", "Muscle Meow.png")
userId = st.session_state.get("user_id", None)
if not userId:
    st.warning("⚠️ No user ID found. Please log in.")
    st.stop()
#def main(userId):
    # Header Section
user_profile = get_user_profile(userId)
st.image(Logo_path, width=100)  
st.title(f"Welcome, {user_profile.get('name', 'Athlete')}! 💪🐾")
st.subheader("Get fit, stay pawsome! 🐱🔥")
value = st.text_input('Enter your name')
data = {
    'NAME': value,
}
components.html(f"""
    <!-- CSS -->
    <style>
        /* Note that the CSS selector matches the HTML class name */
        .custom-component-container {{
            border: 2px solid black;
            padding: 10px;
        }}
    </style>

    <!-- HTML -->
    <div class="custom-component-container">
        <h2>My Custom Component</h2>
        <p>Your name is: {value}</p>
    </div>
""", height=150)
# html_file_name = "my_custom_component"
# create_component(data, html_file_name)

# if __name__ == "__main__":
#     userId = st.session_state.user_id
#     main(userId)