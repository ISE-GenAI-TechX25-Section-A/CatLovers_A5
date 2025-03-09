import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_post


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

if __name__ == "__main__":
    unittest.main()
