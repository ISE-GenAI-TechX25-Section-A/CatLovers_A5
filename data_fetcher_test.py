import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

from data_fetcher import (
    get_user_sensor_data,
    get_user_workouts,
    get_user_profile,
    get_user_posts,
    get_genai_advice
)

class TestDataFetcher(unittest.TestCase):

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        sensor_rows = [
            MagicMock(SensorId="sensor1", Timestamp="2024-01-01 00:00:00", SensorValue=100),
            MagicMock(SensorId="sensor2", Timestamp="2024-01-01 00:01:00", SensorValue=200)
        ]
        type_rows = [
            MagicMock(SensorId="sensor1", Name="heart_rate", Units="bpm"),
            MagicMock(SensorId="sensor2", Name="temperature", Units="C")
        ]

        mock_client.query.return_value.result.side_effect = [
            sensor_rows,  # First query result
            type_rows     # Second query result
        ]

        data = get_user_sensor_data("user123", "workout123")

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["sensor_type"], "heart_rate")
        self.assertEqual(data[1]["units"], "C")

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_row = MagicMock(
            workout_id="w1",
            start_timestamp="2024-01-01 00:00:00",
            end_timestamp="2024-01-01 00:30:00",
            start_lat=1.0,
            start_lng=4.0,
            end_lat=1.1,
            end_lng=4.1,
            distance=5.0,
            steps=1000,
            calories_burned=300
        )
        mock_client.query.return_value.result.return_value = [mock_row]

        workouts = get_user_workouts("user123")
        self.assertEqual(len(workouts), 1)
        self.assertEqual(workouts[0]["workout_id"], "w1")
        self.assertEqual(workouts[0]["distance"], 5.0)

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        user_row = MagicMock(
            Name="Brian Rivera",
            Username="brivera",
            DateOfBirth="2000-01-01",
            ImageUrl="image.jpg"
        )
        friend_row1 = MagicMock(UserId1="user123", UserId2="friend1")
        friend_row2 = MagicMock(UserId1="friend2", UserId2="user123")

        mock_client.query.side_effect = [
            MagicMock(result=lambda: [user_row]),
            MagicMock(__iter__=lambda x: iter([friend_row1, friend_row2]))
        ]

        profile = get_user_profile("user123")
        self.assertEqual(profile["full_name"], "Brian Rivera")
        self.assertIn("friend1", profile["friends"])
        self.assertIn("friend2", profile["friends"])

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_posts(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_row = MagicMock(
            user_id="user123",
            post_id="post123",
            timestamp="2024-01-01 00:00:00",
            content="Hello world",
            image="img.jpg",
            profile_image="profile.jpg"
        )
        mock_client.query.return_value.result.return_value = [mock_row]

        posts = get_user_posts("user123")
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["content"], "Hello world")

    @patch("data_fetcher.bigquery.Client")
    @patch("data_fetcher.model")
    @patch("data_fetcher.random.choice")
    def test_get_genai_advice(self, mock_random_choice, mock_model, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        user_row = MagicMock(Name="Brian", Username="brivera", DateOfBirth="2000-01-01")
        mock_client.query.return_value.result.return_value = [user_row]

        mock_model.generate_content.return_value.text = "Stay strong, Brian!"
        mock_random_choice.return_value = None  # simulate 50/50 image inclusion

        advice = get_genai_advice("user123")

        self.assertIn("advice_id", advice)
        self.assertIn("timestamp", advice)
        self.assertEqual(advice["content"], "Stay strong, Brian!")
        self.assertTrue(advice["image"] in [
            None,
            "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3"
        ])

if __name__ == '__main__':
    unittest.main()
