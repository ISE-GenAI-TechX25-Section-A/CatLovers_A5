import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_user_profile

class TestDisplayUserProfile(unittest.TestCase):

    @patch("streamlit.warning")  
    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="")  # Empty string simulates empty input
    @patch("streamlit.button", return_value=True)
    def test_display_user_profile_empty_input(
        self, mock_button, mock_text_input, mock_markdown, mock_warning
    ):
        """Test behavior when no user ID is entered."""
        display_user_profile({
            'full_name': 'Dummy',
            'username': 'dummy_user',
            'date_of_birth': '2000-01-01',
            'profile_image': '',
            'friends': []
        })

        mock_warning.assert_called_once_with("⚠️ Please enter a valid user ID.")


    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="user1")
    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.write")
    @patch("streamlit.button", return_value=True)
    def test_display_user_profile(self, mock_button, mock_write, mock_subheader,
                                  mock_image, mock_text_input, mock_markdown):
        """Test display of a valid user profile."""

        # Sample mock user data
        mock_user_data = {
            'full_name': 'Remi',
            'username': 'remi_the_rems',
            'date_of_birth': '1990-01-01',
            'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
            'friends': ['user2', 'user3']
        }

        # Call display function with mock data
        display_user_profile(mock_user_data)

        # Header checks
        mock_markdown.assert_any_call("<h1 style='text-align: center; color: orange;'>😺💼 Muscle Meow: User Profile 📋</h1>", unsafe_allow_html=True)
        mock_markdown.assert_any_call("<h3 style='text-align: center; color: gray;'>Every legend starts with a profile. 🔍</h3>", unsafe_allow_html=True)

        # Subheader and main info
        mock_subheader.assert_called_with(f"👤 Profile: {mock_user_data['full_name']} (@{mock_user_data['username']})")
        mock_image.assert_called_with(mock_user_data['profile_image'], caption="Profile Picture", width=250)
        mock_write.assert_any_call(f"**Full Name:** {mock_user_data['full_name']}")
        mock_write.assert_any_call(f"**Username:** {mock_user_data['username']}")
        mock_write.assert_any_call(f"**Date of Birth:** {mock_user_data['date_of_birth']}")
        mock_write.assert_any_call(f"**User ID:** user1")
        mock_write.assert_any_call(f"**Number of Friends:** {len(mock_user_data['friends'])}")

        # Friends section
        mock_markdown.assert_any_call("---")
        mock_markdown.assert_any_call("### 🧑‍🤝‍🧑 Friends")
        for friend in mock_user_data['friends']:
            mock_write.assert_any_call(f"• {friend}")

    @patch("streamlit.error")
    @patch("streamlit.markdown")
    @patch("streamlit.text_input", return_value="invalid_user")
    @patch("streamlit.button", return_value=True)
    def test_display_user_profile_invalid_user(self, mock_button, mock_text_input, mock_markdown, mock_error):
        """Test behavior when an invalid user ID is entered and raises ValueError."""
        # Patch get_user_profile to raise a ValueError
        with patch("modules.get_user_profile", side_effect=ValueError("'invalid_user' was not found.")):
            # Call display function with dummy sample user (won’t be used for invalid input)
            display_user_profile({
                'full_name': 'Dummy',
                'username': 'dummy_user',
                'date_of_birth': '2000-01-01',
                'profile_image': '',
                'friends': []
            })

            # Check for error message
            mock_error.assert_called_with("'invalid_user' was not found.")