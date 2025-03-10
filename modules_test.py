#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.

# Run tests: pytest -p no:warnings modules_test.py
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    @patch('streamlit.image')
    @patch('streamlit.markdown')
    @patch('streamlit.button')
    def test_display_post_renders(self, mock_button, mock_markdown, mock_image):
        """Tests if display_post runs without errors and displays the post correctly."""
        post_info = {
            'post_id': 'post1',
            'user_id': 'remi_the_rems',
            'user_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
            'timestamp': '2024-01-01 00:00:00',
            'content': 'Had a great workout today!',
            'post_image': 'https://i.imgur.com/61ZEkcrb.jpg'
        }

        display_post(post_info)

        # Check if Streamlit elements were called correctly
        mock_image.assert_any_call(post_info['user_image'], width=40)  # Profile picture
        mock_markdown.assert_any_call(f"**{post_info['user_id']}**",  unsafe_allow_html=True)  # Username
        mock_markdown.assert_any_call(f"<small>{post_info['timestamp']}</small>", unsafe_allow_html=True)  # Timestamp
        mock_markdown.assert_any_call(f"<div style='font-size: 14px; margin-top: 10px;'>{post_info['content']}</div>", unsafe_allow_html=True)  # Post content
        mock_image.assert_any_call(post_info['post_image'], width=350)  # Post image
        mock_button.assert_any_call("Like", key=f"like_{post_info['post_id']}")  # Like button
        mock_button.assert_any_call("Comment", key=f"comment_{post_info['post_id']}")  # Comment button


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def setUp(self):
        # Example test data for workouts
        self.workouts_list = [
            {
                'workout_id': 1,
                'start_timestamp': '2025-03-01 08:30:00',
                'end_timestamp': '2025-03-01 09:30:00',
                'start_lat_lng': (37.7749, -122.4194),
                'end_lat_lng': (37.7749, -122.4194),
                'distance': 5.0,  # in km
                'steps': 5000,
                'calories_burned': 300
            },
            {
                'workout_id': 2,
                'start_timestamp': '2025-03-02 15:00:00',
                'end_timestamp': '2025-03-02 16:00:00',
                'start_lat_lng': (37.7749, -122.4194),
                'end_lat_lng': (37.7749, -122.4194),
                'distance': 4.5,  # in km
                'steps': 4500,
                'calories_burned': 280
            }
        ]
    
    @patch('streamlit.metric')
    @patch('streamlit.subheader')
    def test_display_activity_summary(self, mock_subheader, mock_metric):
        # Call the function to test
        display_activity_summary(self.workouts_list)
        print(mock_metric.call_args_list)
        # Check if st.subheader and st.metric were called with expected arguments
        mock_subheader.assert_called_with("Summary")
        #mock_metric.assert_called_with("Average Calories Burned", 290)
        #mock_metric.assert_any_call("Average Distance Travelled", 4.75)
        #mock_metric.assert_any_call("Average Steps Taken", 4750)
        mock_metric.assert_called_with('Average Length of Workouts', '01:00:00')
    


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""
    def setUp(self):
        """Set up example AI advice test data."""
        self.advice = {  
            "timestamp": "2025-03-07",
            "content": "Stay strong and keep pushing!",
            "image": "https://pbs.twimg.com/media/Defa-MqV0AAmaLs.jpg"  
        }
        self.test_advice = {
            "timestamp": self.advice.get("timestamp"),
            "content": self.advice.get("content"),
            "image": self.advice.get("image")
        }

    @patch('streamlit.header')
    @patch('streamlit.markdown')
    @patch('streamlit.write')
    @patch('streamlit.image')

    def test_display_genai_advice_renders(self, mock_image, mock_write, mock_markdown, mock_header):
        display_genai_advice(self.test_advice["timestamp"], self.test_advice["content"], self.test_advice["image"])
        mock_header.assert_called_with("🤖 AI-Generated Advice")
        mock_markdown.assert_called_with(f"**Date:** {self.test_advice['timestamp']}")
        mock_write.assert_called_with(self.test_advice["content"])
        mock_image.assert_called_with(self.test_advice["image"], caption="Stay motivated!", use_container_width=True)

    @patch('streamlit.image')
    def test_display_genai_advice_no_image(self, mock_image):
        display_genai_advice(self.test_advice["timestamp"], self.test_advice["content"], None)
        mock_image.assert_not_called()


    # def test_display_genai_advice_renders(self):
    #     """Tests if display_genai_advice runs without errors and displays advice correctly."""
    #     app = AppTest(display_genai_advice, args=("2025-03-07", "Stay strong and keep pushing!", None))
    #     self.assertFalse(app.exception)  
    #     self.assertIn("Stay strong and keep pushing!", app.html)  
    #     self.assertIn("2025-03-07", app.html)  


class TestDisplayRecentWorkouts(unittest.TestCase):

    def setUp(self):
        """Set up sample workout data for testing."""
        self.workouts = [
            {
                "workout_id": "W123",
                "start_timestamp": "2025-03-07 08:00:00",
                "end_timestamp": "2025-03-07 09:00:00",
                "distance": 5.0,
                "steps": 6000,
                "calories_burned": 450,
                "start_lat_lng": "18.4655, -66.1057",
                "end_lat_lng": "18.4665, -66.1067"
            }
        ]

    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="user1")
    @patch("streamlit.warning")
    @patch("streamlit.button", return_value=False)
    def test_display_recent_workouts_initial_state(self, mock_button, mock_warning, mock_text_input, mock_markdown):
        """Tests the UI elements rendering when no button press occurs."""
        display_recent_workouts(self.workouts)
        mock_markdown.assert_any_call("<h1 style='text-align: center; color: orange;'>🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️</h1>", unsafe_allow_html=True)
        mock_text_input.assert_called_with("🔍 Enter user ID", "user1")
        mock_button.assert_called_with("🐾Show Recent Workouts🐾")
        mock_warning.assert_not_called()

    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="")
    @patch("streamlit.warning")
    @patch("streamlit.button", return_value=True)
    def test_display_recent_workouts_empty_user_id(self, mock_button, mock_warning, mock_text_input, mock_markdown):
        """Tests behavior when user ID is empty."""
        display_recent_workouts(self.workouts)
        mock_warning.assert_called_with("⚠️ Please enter a valid user ID.")

    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="user1")
    @patch("streamlit.button", return_value=True)
    @patch("streamlit.subheader")
    @patch("streamlit.expander")
    @patch("streamlit.write")
    def test_display_recent_workouts_with_data(self, mock_write, mock_expander, mock_subheader, mock_button, mock_text_input, mock_markdown):
        """Tests if workout data is displayed correctly when button is pressed."""
        mock_expander_instance = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_instance
        display_recent_workouts(self.workouts)
        
        mock_subheader.assert_called_with("user1's Recent Workouts Overview")
        mock_expander.assert_called_with("Workout ID: W123")
        mock_write.assert_any_call("**Start Time:** 2025-03-07 08:00:00")
        mock_write.assert_any_call("**End Time:** 2025-03-07 09:00:00")
        mock_write.assert_any_call("**Distance:** 5.0 km")
        mock_write.assert_any_call("**Steps Taken:** 6000")
        mock_write.assert_any_call("**Calories Burned:** 450 kcal")

    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="user1")
    @patch("streamlit.button", return_value=True)
    @patch("streamlit.subheader")
    @patch("streamlit.info")
    def test_display_recent_workouts_no_data(self, mock_info, mock_subheader, mock_button, mock_text_input, mock_markdown):
        """Tests if the function correctly handles cases where no workouts are found."""
        display_recent_workouts([])
        mock_subheader.assert_called_with("user1's Recent Workouts Overview")
        mock_info.assert_called_with("No recent workouts found.")


if __name__ == "__main__":
    unittest.main()
