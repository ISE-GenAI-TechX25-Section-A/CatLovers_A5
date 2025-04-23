#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.

# Run tests: pytest -p no:warnings modules_test.py
#############################################################################
import unittest
import runpy
from unittest.mock import patch, MagicMock, Mock
from streamlit.testing.v1 import AppTest
import statistics
from datetime import datetime, timedelta
import streamlit as st
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts, display_user_profile, display_streak_tracker, display_buff_cat_points, display_goal_creation_ui, display_goal_progress_bars, track_added_goals, track_checked_goals, display_exercise_card, display_exercises_list
from unittest.mock import call
from types import SimpleNamespace

# Write your tests below

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
    def test_switch_page_called(self, mock_get_user_workouts, mock_button, mock_switch_page):
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
            'workout_id': 'W123',
            'start_timestamp': '2025-03-07 08:00:00',
            'end_timestamp': '2025-03-07 09:00:00',
            'distance': 5.0,
            'steps': 6000,
            'calories_burned': 450,
            'start_lat_lng': {'lat': 18.4665, 'lng': -66.1067},
            'end_lat_lng': {'lat': 18.4670, 'lng': -66.1070}
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
        mock_write.assert_any_call("**Start Location (Lat, Lng):** (18.4665,-66.1067)")
        mock_write.assert_any_call("**End Location (Lat, Lng):** (18.467,-66.107)")

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


class TestDisplayBuffCatPoints(unittest.TestCase):

    @patch("modules.st.markdown")  # Mocking Streamlit markdown
    def test_display_buff_cat_points_calls_markdown(self, mock_markdown):
        user_id = 123  # Example ID
        display_buff_cat_points(user_id)

        # Assert that markdown was called at least twice
        self.assertGreaterEqual(mock_markdown.call_count, 2)

        calls = [call.args[0] for call in mock_markdown.call_args_list]
        points_html_found = any("⭐ 120 Points" in call for call in calls)
        self.assertTrue(points_html_found, "Expected point display HTML not found")

class TestDisplayGoalCreationUI(unittest.TestCase):
    @patch("modules.st")
    @patch("modules.time.sleep")  
    def test_display_goal_creation_ui_initializes_session_state(self, mock_sleep, mock_st):
        # Mock Streamlit session_state
        mock_st.session_state = {}
        # Mock return values for st UI components
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.selectbox.return_value = "Legs"
        mock_st.text_input.return_value = "Test Goal"
        mock_st.button.return_value = False  # Simulate no button click

        # Run the function
        display_goal_creation_ui()

        # Check that session state keys were initialized
        expected_keys = [
            "total_daily_goals", "checked_daily_goals",
            "total_weekly_goals", "checked_weekly_goals",
            "total_monthly_goals", "checked_monthly_goals",
            "goal_data"
        ]
        for key in expected_keys:
            self.assertIn(key, mock_st.session_state)

        # Ensure goal_data contains all 3 timeframes
        self.assertEqual(mock_st.session_state["goal_data"], {
            "Daily": [],
            "Weekly": [],
            "Monthly": []
        })

        # Assert tabs creation
        mock_st.tabs.assert_called_once_with(["📆 Daily", "📈 Weekly", "📊 Monthly"])

        # Confirm selectbox was called 
        self.assertTrue(mock_st.selectbox.called)

class TestDisplayGoalProgressBars(unittest.TestCase):

    @patch("modules.st")
    def test_display_goal_progress_bars_with_values(self, mock_st):
        # Set up mock session state with sample values
        mock_st.session_state = {
            "total_daily_goals": 4,
            "checked_daily_goals": 2,
            "total_weekly_goals": 5,
            "checked_weekly_goals": 3,
            "total_monthly_goals": 10,
            "checked_monthly_goals": 5
        }
        display_goal_progress_bars("user123")

        # Check that progress bars were called with correct percentages
        mock_st.markdown.assert_called_with("### 🎯 Goal Progress")
        mock_st.progress.assert_any_call(0.5, text="Daily Progress")   # 2/4
        mock_st.progress.assert_any_call(0.6, text="Weekly Progress")  # 3/5
        mock_st.progress.assert_any_call(0.5, text="Monthly Progress") # 5/10

    @patch("modules.st")
    def test_display_goal_progress_bars_with_zeros(self, mock_st):
        # Simulate a case where no goals are set
        mock_st.session_state = {
            "total_daily_goals": 0,
            "checked_daily_goals": 0,
            "total_weekly_goals": 0,
            "checked_weekly_goals": 0,
            "total_monthly_goals": 0,
            "checked_monthly_goals": 0
        }

        display_goal_progress_bars("user123")
        # Should not raise division by zero
        mock_st.progress.assert_any_call(0, text="Daily Progress")
        mock_st.progress.assert_any_call(0, text="Weekly Progress")
        mock_st.progress.assert_any_call(0, text="Monthly Progress")

class TestTrackGoals(unittest.TestCase):

    @patch("modules.st")
    def test_track_added_goals_daily(self, mock_st):
        mock_st.session_state = SimpleNamespace(total_daily_goals=0)
        mock_st.write = MagicMock()
        track_added_goals("daily")

        self.assertEqual(mock_st.session_state.total_daily_goals, 1)
        mock_st.write.assert_called_with(1)

    @patch("modules.st")
    def test_track_added_goals_weekly(self, mock_st):
        mock_st.session_state = SimpleNamespace(total_weekly_goals=2)
        mock_st.write = MagicMock()
        track_added_goals("weekly")

        self.assertEqual(mock_st.session_state.total_weekly_goals, 3)
        mock_st.write.assert_not_called()

    @patch("modules.st")
    def test_track_added_goals_monthly(self, mock_st):
        mock_st.session_state = SimpleNamespace(total_monthly_goals=5)
        mock_st.write = MagicMock()
        track_added_goals("monthly")

        self.assertEqual(mock_st.session_state.total_monthly_goals, 6)
        mock_st.write.assert_not_called()

    @patch("modules.st")
    def test_track_checked_goals_daily(self, mock_st):
        mock_st.session_state = SimpleNamespace(checked_daily_goals=0)
        mock_st.write = MagicMock()
        track_checked_goals("daily")

        self.assertEqual(mock_st.session_state.checked_daily_goals, 1)
        mock_st.write.assert_called_with(1)

    @patch("modules.st")
    def test_track_checked_goals_weekly(self, mock_st):
        mock_st.session_state = SimpleNamespace(checked_weekly_goals=1)
        mock_st.write = MagicMock()
        track_checked_goals("weekly")

        self.assertEqual(mock_st.session_state.checked_weekly_goals, 2)
        mock_st.write.assert_not_called()

    @patch("modules.st")
    def test_track_checked_goals_monthly(self, mock_st):
        mock_st.session_state = SimpleNamespace(checked_monthly_goals=3)
        mock_st.write = MagicMock()
        track_checked_goals("monthly")

        self.assertEqual(mock_st.session_state.checked_monthly_goals, 4)
        mock_st.write.assert_not_called()

class TestExerciseDisplay(unittest.TestCase):

    @patch("modules.st.container")
    @patch("modules.st.markdown")
    @patch("modules.st.checkbox")
    @patch("modules.st.expander")
    def test_display_exercise_card(self, mock_expander, mock_checkbox, mock_markdown, mock_container):
        # Mock exercise data
        exercise = {
            'gifUrl': 'https://example.com/gif.jpg',
            'name': 'Push-Up',
            'target': 'Chest',
            'equipment': 'None',
            'instructions': ['Step 1', 'Step 2', 'Step 3']
        }

        mock_checkbox.return_value = True  # Simulate checkbox being selected
        selected = display_exercise_card(exercise, key_prefix="test")

        # Check that checkbox was called with the correct key
        mock_checkbox.assert_called_with("Select this exercise", key="test_selected")

        # Check that markdown (HTML) for exercise card was generated
        expected_html = '''
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
                <img src="https://example.com/gif.jpg" style="width:150px; height:150px; border-radius: 10px;" />
                <h4 style="margin-top: 1rem;">Push-Up</h4>
                <p><strong>Target:</strong> Chest</p>
                <p><strong>Equipment:</strong> None</p>
            </div>
            '''
        mock_markdown.assert_any_call(expected_html, unsafe_allow_html=True)
        # Check that instructions were displayed
        for step in exercise["instructions"]:
            mock_markdown.assert_any_call(f"- {step}")

        self.assertTrue(selected)

    @patch("modules.st.title")
    @patch("modules.st.subheader")
    @patch("modules.st.markdown")
    @patch("modules.st.checkbox")
    @patch("modules.st.container")
    @patch("modules.st.expander")
    def test_display_exercises_list(self, mock_expander, mock_container, mock_checkbox, mock_markdown, mock_subheader, mock_title):
        # Mock a list of exercises
        exercises = [
            {'gifUrl': 'https://example.com/gif1.jpg', 'name': 'Push-Up', 'target': 'Chest', 'equipment': 'None', 'instructions': ['Step 1', 'Step 2']},
            {'gifUrl': 'https://example.com/gif2.jpg', 'name': 'Squat', 'target': 'Legs', 'equipment': 'None', 'instructions': ['Step 1', 'Step 2']},
        ]
        mock_checkbox.return_value = True  # Simulate both checkboxes being selected
        display_exercises_list(exercises)
        mock_title.assert_called_once_with("💪 Browse Exercises")
        # Check that display_exercise_card was called for each exercise
        for i, exercise in enumerate(exercises):
            mock_container.assert_called()
            mock_checkbox.assert_any_call("Select this exercise", key=f"ex_{i}_selected")

        mock_subheader.assert_called_with("✅ Selected Exercises:")
        for exercise in exercises:
            mock_markdown.assert_any_call(f"- {exercise['name']}")

if __name__ == "__main__":
    unittest.main()
