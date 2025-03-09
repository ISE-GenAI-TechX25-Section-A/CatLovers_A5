import unittest
from unittest.mock import patch
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_activity_summary



class TestDisplayActivitySummary(unittest.TestCase):
    
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
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.caption')
    @patch('streamlit.bar_chart')
    def test_display_activity_summary(self, mock_bar_chart, mock_caption, mock_metric, mock_columns):
        # Mock the columns to avoid actual Streamlit layout behavior
        mock_columns.return_value = [None, None]  # Mock two columns

        # Call the function to test
        display_activity_summary(self.workouts_list)

        # Test if the average distance was calculated correctly
        avg_distances = statistics.mean([workout['distance'] for workout in self.workouts_list])
        mock_metric.assert_any_call("Average Distance Travelled", avg_distances)

        # Test if the average calories was calculated correctly
        avg_calories = statistics.mean([workout['calories_burned'] for workout in self.workouts_list])
        mock_metric.assert_any_call("Average Calories Burned", avg_calories)

        # Test if the average steps was calculated correctly
        avg_steps = statistics.mean([workout['steps'] for workout in self.workouts_list])
        mock_metric.assert_any_call("Average Steps Taken", avg_steps)

        # Test if the favorite time of day was calculated correctly
        fav_time_of_day = "Morning"  # Based on the test data
        mock_metric.assert_any_call("Favorite Time of Day", fav_time_of_day)

        # Test if the favorite day of the week was calculated correctly
        fav_day_of_week = "Monday"  # Based on the test data
        mock_metric.assert_any_call("Favorite Day of Week", fav_day_of_week)

        # Test if workout length is calculated correctly
        # Calculate the expected workout length manually
        lengths = [
            (datetime.strptime(workout['end_timestamp'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(workout['start_timestamp'], "%Y-%m-%d %H:%M:%S")).total_seconds()
            for workout in self.workouts_list
        ]
        avg_seconds = statistics.mean(lengths)
        avg_duration = timedelta(seconds=avg_seconds)
        hours, remainder = divmod(avg_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        workoutLength = f"{hours:02}:{minutes:02}:{seconds:02}"

        mock_metric.assert_any_call("Average Length of Workouts", workoutLength)

        # Test if caption is correctly called
        mock_caption.assert_called_with(f"Congratulations! Your favorite time to workout is {fav_time_of_day}. You work out most on {fav_day_of_week}. You burn an average of {avg_calories} calories in {workoutLength} time.")

        # Test if the bar chart is called
        mock_bar_chart.assert_called_once()

if __name__ == '__main__':
    unittest.main()
