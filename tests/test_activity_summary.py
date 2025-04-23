import unittest
from unittest.mock import patch
import statistics
from datetime import datetime, timedelta
import streamlit as st
import runpy

"""Run tests: PYTHONPATH=. pytest tests/test_activity_summary.py"""

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function.
    Tests for correct formatting by ChatGPT
    """

    @patch('streamlit.metric')
    @patch('streamlit.subheader')
    @patch('streamlit.button')
    @patch('streamlit.write')
    @patch('streamlit.markdown')
    @patch('streamlit.bar_chart')
    @patch('data_fetcher.get_user_workouts')
    @patch('streamlit.session_state', {'user_id': 'test_user'})
    def test_display_activity_summary(self, mock_get_user_workouts, mock_bar_chart, mock_markdown, mock_write, mock_button, mock_subheader, mock_metric):
        # Example test data for workouts
        mock_get_user_workouts.return_value = [
            {
                'workout_id': 1,
                'start_timestamp': datetime.fromisoformat("2024-07-29T07:00:00"),
                'end_timestamp': datetime.fromisoformat("2024-07-29T08:00:00"),
                'start_lat_lng': (37.7749, -122.4194),
                'end_lat_lng': (37.7749, -122.4194),
                'distance': 5.0,  # in km
                'steps': 5000,
                'calories_burned': 300
            },
            {
                'workout_id': 2,
                'start_timestamp': datetime.fromisoformat("2024-07-29T18:00:00"),
                'end_timestamp': datetime.fromisoformat("2024-07-29T19:00:00"),
                'start_lat_lng': (37.7749, -122.4194),
                'end_lat_lng': (37.7749, -122.4194),
                'distance': 4.5,  # in km
                'steps': 4500,
                'calories_burned': 280
            }
        ]
        
        
        # Separate test for button behavior
        mock_button.return_value = False
        
        # Run the script
        runpy.run_path("pages/workout_summary_page.py", run_name="__main__")

        # Call the function to test
        # display_activity_summary(self.workouts_list)
        #print(mock_button.call_args_list)


        mock_markdown.assert_any_call("### 🏃 Recent Workouts")
        mock_markdown.assert_any_call("### 📊 Activity Summary")
        mock_markdown.assert_any_call("### ✨ Stats")
        mock_metric.assert_any_call("Average Calories Burned", 290)
        mock_metric.assert_any_call("Average Distance Travelled", 4.75)
        mock_metric.assert_any_call("Average Steps Taken", 4750)
        mock_metric.assert_any_call("Favorite Time of Day", "Morning")
        mock_metric.assert_any_call("Favorite Day of Week", "Monday")
        mock_metric.assert_any_call('Average Length of Workouts', '01:00:00')
        mock_metric_call_count = 6
        # Inspect call arguments to verify formatting
        for call in mock_metric.call_args_list:
            label, value = call[0]
            assert isinstance(label, str)  # Check label is a string
            assert isinstance(value, (int, float, str))  # Ensure value is numeric
        
        # checking for correct variables while ignoring whitespace discrepancies
        expected_content = [
            "<b>Morning</b>",
            "<b>Monday</b>",
            "<b>290</b>",
            "<b>01:00:00</b>"
        ]
        
        # collect the markdown texts from the calls
        called_texts = [call.args[0] for call in mock_markdown.call_args_list]

        # assert that at least one call contains all the expected parts
        assert any(all(part in text for part in expected_content) for text in called_texts), "Expected markdown call not found"

        # setting up variables to match mock workout_tests
        monday = 2
        tuesday = 0
        wednesday = 0
        thursday = 0
        friday = 0
        saturday = 0
        sunday = 0
        days_of_week = {"Monday":monday, "Tuesday":tuesday, "Wednesday":wednesday, "Thursday":thursday, "Friday":friday, "Saturday":saturday, "Sunday":sunday}
        

        mock_bar_chart.assert_any_call(days_of_week, x_label="Weekday", y_label="Frequency")
        mock_bar_chart_call_count = 1

@patch("streamlit.switch_page")
@patch("streamlit.button")
@patch('data_fetcher.get_user_workouts')
def test_switch_page_called(mock_get_user_workouts, mock_button, mock_switch_page):
    # Example test data for workouts
    mock_get_user_workouts.return_value = [
        {
            'workout_id': 1,
            'start_timestamp': datetime.fromisoformat("2024-07-29T07:00:00"),
            'end_timestamp': datetime.fromisoformat("2024-07-29T08:00:00"),
            'start_lat_lng': (37.7749, -122.4194),
            'end_lat_lng': (37.7749, -122.4194),
            'distance': 5.0,  # in km
            'steps': 5000,
            'calories_burned': 300
        },
        {
            'workout_id': 2,
            'start_timestamp': datetime.fromisoformat("2024-07-29T18:00:00"),
            'end_timestamp': datetime.fromisoformat("2024-07-29T19:00:00"),
            'start_lat_lng': (37.7749, -122.4194),
            'end_lat_lng': (37.7749, -122.4194),
            'distance': 4.5,  # in km
            'steps': 4500,
            'calories_burned': 280
        }
    ]

    mock_button.return_value = True

    # Run the script (same as if user clicked "See More")
    runpy.run_path("pages/workout_summary_page.py", run_name="__main__")

    # Check if elements were called with expected arguments
    mock_button.assert_any_call("See More")

    # Check that switch_page was triggered
    mock_switch_page.assert_called_once_with("pages/recent_workouts_page.py")

if __name__ == '__main__':
    unittest.main()
