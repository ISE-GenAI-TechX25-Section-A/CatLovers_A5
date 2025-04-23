import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from modules import display_streak_tracker
class TestDisplayStreakTracker(unittest.TestCase):

    @patch("modules.get_user_workouts")
    @patch("modules.st.markdown")
    def test_one_week_streak(self, mock_markdown, mock_get_user_workouts):
        base_date = datetime(2025, 4, 1)
        mock_get_user_workouts.return_value = [
            {"start_timestamp": base_date + timedelta(days=i)} for i in range(7)
        ]
        
        display_streak_tracker("user123")

        self.assertIn("7 days", mock_markdown.call_args[0][0])
        self.assertIn("earned 5 Buff Cat Points", mock_markdown.call_args[0][0])

    @patch("modules.get_user_workouts")
    @patch("modules.st.markdown")
    def test_no_streak(self, mock_markdown, mock_get_user_workouts):
        mock_get_user_workouts.return_value = []

        display_streak_tracker("user123")

        self.assertIn("0 days", mock_markdown.call_args[0][0])

    @patch("modules.get_user_workouts")
    @patch("modules.st.markdown")
    def test_thirty_day_streak(self, mock_markdown, mock_get_user_workouts):
        base_date = datetime(2025, 1, 1)
        mock_get_user_workouts.return_value = [
            {"start_timestamp": base_date + timedelta(days=i)} for i in range(30)
        ]
        
        display_streak_tracker("user456")

        self.assertIn("30 days", mock_markdown.call_args[0][0])
        self.assertIn("earned 15 Buff Cat Points", mock_markdown.call_args[0][0])

