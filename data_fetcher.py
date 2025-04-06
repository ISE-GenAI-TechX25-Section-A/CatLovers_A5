#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#############################################################################

import os
import random
import uuid
from datetime import datetime
from google.cloud import bigquery
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables
load_dotenv()

# Initialize Vertex AI
vertexai.init(project=os.getenv("PROJECT_ID"), location="us-central1")

# Load the generative model
model = GenerativeModel("gemini-2.0-flash-001")

# --- Dummy user data ---
users = {
    'user1': {
        'full_name': 'Remi',
        'username': 'remi_the_rems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user2', 'user3', 'user4'],
    },
    'user2': {
        'full_name': 'Blake',
        'username': 'blake',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1'],
    },
    'user3': {
        'full_name': 'Jordan',
        'username': 'jordanjordanjordan',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user4'],
    },
    'user4': {
        'full_name': 'Gemmy',
        'username': 'gems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user3'],
    },
}


def get_user_sensor_data(user_id, workout_id):
    """Returns dummy timestamped sensor data for a workout."""
    sensor_data = []
    sensor_types = ['accelerometer', 'gyroscope', 'pressure', 'temperature', 'heart_rate']
    for _ in range(random.randint(5, 100)):
        minute = f"{random.randint(0, 59):02}"
        timestamp = f"2024-01-01 00:{minute}:00"
        sensor_data.append({
            'sensor_type': random.choice(sensor_types),
            'timestamp': timestamp,
            'data': random.random() * 100,
            'units': 'unit'
        })
    return sensor_data


def get_user_workouts(user_id):
    """Fetch workouts from BigQuery."""
    client = bigquery.Client(project=os.getenv("PROJECT_ID"))
    query = """
        SELECT WorkoutId AS workout_id, StartTimestamp AS start_timestamp, EndTimestamp AS end_timestamp,
               StartLocationLat AS start_lat, StartLocationLong AS start_lng,
               EndLocationLat AS end_lat, EndLocationLong AS end_lng,
               TotalDistance AS distance, TotalSteps AS steps, CaloriesBurned AS calories_burned
        FROM `brianrivera26techx25.ISE.Workouts`
        WHERE UserId = @user_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    results = client.query(query, job_config=job_config).result()
    workouts = []
    for row in results:
        workouts.append({
            'workout_id': row.workout_id,
            'start_timestamp': row.start_timestamp,
            'end_timestamp': row.end_timestamp,
            'start_lat_lng': {'lat': row.start_lat, 'lng': row.start_lng},
            'end_lat_lng': {'lat': row.end_lat, 'lng': row.end_lng},
            'distance': row.distance,
            'steps': row.steps,
            'calories_burned': row.calories_burned
        })
    return workouts


def get_user_profile(user_id):
    """Returns static user profile info from dummy dictionary."""
    if user_id not in users:
        raise ValueError(f"User {user_id} not found.")
    return users[user_id]


def get_user_posts(user_id):
    """Returns a single dummy post for a user."""
    content = random.choice([
        'Had a great workout today!',
        'The AI really motivated me to push myself further, I ran 10 miles!'
    ])
    user_info = get_user_profile(user_id)
    return {
        'user_id': user_info['username'],
        'post_id': 'post1',
        'timestamp': '2024-01-01 00:00:00',
        'content': content,
        'user_image': user_info['profile_image'],
        'post_image': 'https://i.imgur.com/61ZEkcrb.jpg',
    }


def get_genai_advice(user_id):
    """Returns motivational advice generated via Vertex AI."""
    try:
        client = bigquery.Client(project=os.getenv("PROJECT_ID"))
        query = """
            SELECT Name, Username, DateOfBirth
            FROM `brianrivera26techx25.ISE.Users`
            WHERE UserId = @user_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
        )
        results = list(client.query(query, job_config=job_config).result())
        if not results:
            return None

        user = results[0]
        prompt = (
            f"Give one short motivational fitness tip to a user named {user['Name']} "
            f"(username: @{user['Username']}), born on {user['DateOfBirth']}. Keep it fun and inspiring!"
        )

        response = model.generate_content(prompt)

        return {
            'advice_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'content': response.text.strip(),
            'image': random.choice([
                'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3',
                None
            ])
        }

    except Exception as e:
        return {
            'advice_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'content': f"😴 The cat is too sleepy to give advice right now... (Error: {str(e)})",
            'image': None
        }
