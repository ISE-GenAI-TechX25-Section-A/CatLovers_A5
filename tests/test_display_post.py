import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_post


class TestDisplayPost(unittest.TestCase):
    def setUp(self):
        # Example test data for posts
        self.post_info = {
                    'post_id': 'post1',
                    'user_id': 'remi_the_rems',
                    'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
                    'timestamp': '2024-01-01 00:00:00',
                    'content': 'Had a great workout today!',
                    'image': 'https://i.imgur.com/61ZEkcrb.jpg'
                        }
    """Tests the display_post function."""

    @patch('streamlit.image')
    @patch('streamlit.markdown')
    @patch('streamlit.button')
    def test_display_post_renders(self, mock_button, mock_markdown, mock_image):
        """Tests if display_post runs without errors and displays the post correctly."""
            
        display_post(self.post_info)

        # Check if Streamlit elements were called correctly
        mock_image.assert_any_call(self.post_info['profile_image'], width=40)  # Profile picture
        mock_markdown.assert_any_call(f"**{self.post_info['user_id']}**",  unsafe_allow_html=True)  # Username
        mock_markdown.assert_any_call(f"<small>{self.post_info['timestamp']}</small>", unsafe_allow_html=True)  # Timestamp
        mock_markdown.assert_any_call(f"<div style='font-size: 14px; margin-top: 10px;'>{self.post_info['content']}</div>", unsafe_allow_html=True)  # Post content
        mock_image.assert_any_call(self.post_info['image'], width=350)  # Post image
        mock_button.assert_any_call("Like", key=f"like_{self.post_info['post_id']}_{0}")  # Like button
        mock_button.assert_any_call("Comment", key=f"comment_{self.post_info['post_id']}_{0}")  # Comment button



if __name__ == "__main__":
    unittest.main()
