#############################################################################
# data_fetcher.py
<<<<<<< HEAD
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
load_dotenv()

vertexai.init(project=os.getenv("PROJECT_ID"), location="us-central1")

model = GenerativeModel("gemini-2.0-flash-001")
=======
#############################################################################
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import os
import uuid
import random
from datetime import datetime
>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)

# === Setup credentials and project info ===
KEY_PATH = os.path.expanduser("~/.gcp_keys/vertex-access-key.json")
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

PROJECT_ID = "brianrivera26techx25"
LOCATION = "us-central1"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

# === Import Vertex AI after credentials ===
from vertexai import init as vertex_init
from vertexai.preview.language_models import TextGenerationModel

vertex_init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
model = TextGenerationModel.from_pretrained("text-bison@001")

# === Functions ===

<<<<<<< HEAD

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
=======
def get_user_sensor_data(user_id, workout_id):
    client = bigquery.Client(project=PROJECT_ID, credentials=credentials, location="US")
    sensor_data_table = f"{PROJECT_ID}.ISE.SensorData"
    sensor_type_table = f"{PROJECT_ID}.ISE.SensorTypes"

    query = f"SELECT * FROM `{sensor_data_table}` WHERE WorkoutID = @workout_id"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)]
    )
    results = client.query(query, job_config=job_config).result()

    sensor_data, sensors, timestamp, data = [], [], [], []

    for row in results:
        sensors.append(row.SensorId)
        timestamp.append(row.Timestamp)
        data.append(row.SensorValue)

    sensor_type = [None] * len(sensors)
    unit = [None] * len(sensors)

    sensor_type_results = client.query(f"SELECT * FROM `{sensor_type_table}`").result()
    for row in sensor_type_results:
        if row.SensorId in sensors:
            index = sensors.index(row.SensorId)
            sensor_type[index] = row.Name
            unit[index] = row.Units

    for i in range(len(sensors)):
        sensor_data.append({
            'sensor_type': sensor_type[i],
            'timestamp': timestamp[i],
            'data': data[i],
            'units': unit[i]
        })

>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
    return sensor_data


def get_user_workouts(user_id):
<<<<<<< HEAD
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
=======
    client = bigquery.Client(project=PROJECT_ID, credentials=credentials, location="US")

    query = f"""
        SELECT
            WorkoutId AS workout_id,
            StartTimestamp AS start_timestamp,
            EndTimestamp AS end_timestamp,
            StartLocationLat AS start_lat,
            StartLocationLong AS start_lng,
            EndLocationLat AS end_lat,
            EndLocationLong AS end_lng,
            TotalDistance AS distance,
            TotalSteps AS steps,
            CaloriesBurned AS calories_burned
        FROM
            `{PROJECT_ID}.ISE.Workouts`  
        WHERE
            UserId = @user_id
    """

>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    results = client.query(query, job_config=job_config).result()
<<<<<<< HEAD
=======

>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
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
<<<<<<< HEAD
=======

>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
    return workouts


def get_user_profile(user_id):
<<<<<<< HEAD
    """Returns static user profile info from dummy dictionary."""
    if user_id not in users:
        raise ValueError(f"User {user_id} not found.")
    return users[user_id]


def get_user_posts(user_id):
    """Returns a single dummy post for a user."""
=======
    client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

    query = f"""
        SELECT UserId, Name, Username, ImageUrl, DateOfBirth
        FROM `{PROJECT_ID}.ISE.Users`
        WHERE UserId = @user_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    user_result = list(client.query(query, job_config=job_config).result())

    if not user_result:
        raise ValueError(f"User '{user_id}' not found.")

    user_row = user_result[0]

    friends_query = f"""
        SELECT UserId1, UserId2
        FROM `{PROJECT_ID}.ISE.Friends`
        WHERE UserId1 = @user_id OR UserId2 = @user_id
    """
    friends_job = client.query(friends_query, job_config=job_config)
    friends = set()
    for row in friends_job:
        friends.add(row.UserId2 if row.UserId1 == user_id else row.UserId1)

    return {
        'full_name': user_row.Name,
        'username': user_row.Username,
        'date_of_birth': str(user_row.DateOfBirth),
        'profile_image': user_row.ImageUrl,
        'friends': list(friends)
    }


def get_user_posts(user_id):
>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
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
<<<<<<< HEAD
    """Returns motivational advice generated via Vertex AI."""
    try:
        client = bigquery.Client(project=os.getenv("PROJECT_ID"))
        query = """
            SELECT Name, Username, DateOfBirth
            FROM `brianrivera26techx25.ISE.Users`
=======
    try:
        client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

        query = f"""
            SELECT Name, Username, DateOfBirth
            FROM `{PROJECT_ID}.ISE.Users`
>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
            WHERE UserId = @user_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
        )
        results = list(client.query(query, job_config=job_config).result())
<<<<<<< HEAD
=======

>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
        if not results:
            return None

        user = results[0]
<<<<<<< HEAD
        prompt = (
            f"Give one short motivational fitness tip to a user named {user['Name']} "
            f"(username: @{user['Username']}), born on {user['DateOfBirth']}. Keep it fun and inspiring!"
        )

        response = model.generate_content(prompt)
=======
        prompt = f"Give one short motivational fitness tip to a user named {user['Name']} (username: @{user['Username']}), born on {user['DateOfBirth']}. Keep it fun and inspiring!"
        response = model.predict(prompt, temperature=0.7, max_output_tokens=80)
>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)

        return {
            'advice_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'content': response.text.strip(),
            'image': random.choice([
<<<<<<< HEAD
                'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3',
                None
            ])
        }

    except Exception as e:
        return {
            'advice_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'content': f"😴 The cat is too sleepy to give advice right now... (Error: {str(e)})",
=======
                'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop',
                None,
            ]),
        }

    except Exception as e:
        st.warning(f"⚠️ Could not retrieve AI advice: {e}")
        return {
            'advice_id': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'content': "We couldn't fetch AI advice right now 😿",
>>>>>>> 9ac6b93 (Fix Vertex AI error handling and update data_fetcher logic)
            'image': None
        }
