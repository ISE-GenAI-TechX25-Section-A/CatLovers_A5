#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.

# Run tests: pytest -p no:warnings modules_test.py
#############################################################################
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


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

    # def test_display_genai_advice_renders(self):
    #     """Tests if display_genai_advice runs without errors and displays advice correctly."""
    #     app = AppTest(display_genai_advice, args=("2025-03-07", "Stay strong and keep pushing!", None))
    #     self.assertFalse(app.exception)  
    #     self.assertIn("Stay strong and keep pushing!", app.html)  
    #     self.assertIn("2025-03-07", app.html)  


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
