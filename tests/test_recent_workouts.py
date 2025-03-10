import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from modules import display_recent_workouts

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