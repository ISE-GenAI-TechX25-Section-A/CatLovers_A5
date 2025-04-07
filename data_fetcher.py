#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#############################################################################
from google.cloud import bigquery
import random
import streamlit as st

import os
import random
import uuid
from datetime import datetime
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables
load_dotenv()

# Initialize Vertex AI
vertexai.init(project="brianrivera26techx25", location="us-central1")

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

#used for individual workouts in "recent workouts"
def get_user_sensor_data(user_id, workout_id):
    """
    Returns a list of timestamped information for a given workout. 
    Input: user_id, workout_id
    Output: A list of sensor data from the workout. Each item in the list is a dictionary with keys sensor_type, timestamp, data, units

    """

    """
    Use the workout_id to get which sensor it is and the sensor value and the timestamp. There will be multiple sensors for each workout. 
    Use the sensor_id to get the sensor type and units
    
    sensor_type = sensor type
    timestamp = timestamp
    data = sensor value
    units = units

    Each item in the list will be a sensor. Sensor will be a dictionary with the above keys and values

    """
    

    client = bigquery.Client(project="brianrivera26techx25",location="US")
    sensor_data_table = "brianrivera26techx25.ISE.SensorData"
    sensor_type_table = "brianrivera26techx25.ISE.SensorTypes"

    query = f"""
        SELECT *
        FROM `{sensor_data_table}`
        WHERE WorkoutID = @workout_id
        """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)
        ]
    )

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    sensor_data = []
    sensors = []
    timestamp = []
    data = []

    for row in results:
        sensors.append(row.SensorId)
        timestamp.append(row.Timestamp)
        data.append(row.SensorValue)

    sensor_type = [None] * len(sensors)
    unit = [None] * len(sensors)

    another_table = client.query(
        f"""
        SELECT *
        FROM {sensor_type_table}
        """
    ).result()

    for row in another_table:
        index = sensors.index(row.SensorId)
        sensor_type[index] = row.Name
        unit[index] = row.Units

    for i in range(len(sensors)):
        sensor_data.append(
            {'sensor_type': sensor_type[i], 'timestamp': timestamp[i], 'data': data[i], 'units': unit[i]}
        )
        
    return sensor_data

    

    # sensor_data = []
    # sensor_types = [
    #     'accelerometer',
    #     'gyroscope',
    #     'pressure',
    #     'temperature',
    #     'heart_rate',
    # ]
    # for index in range(random.randint(5, 100)):
    #     random_minute = str(random.randint(0, 59))
    #     if len(random_minute) == 1:
    #         random_minute = '0' + random_minute
    #     timestamp = '2024-01-01 00:' + random_minute + ':00'
    #     data = random.random() * 100
    #     sensor_type = random.choice(sensor_types)
    #     sensor_data.append(
    #         {'sensor_type': sensor_type, 'timestamp': timestamp, 'data': data}
    #     )
    # print(sensor_data)
    # return sensor_data


# def get_user_workouts(user_id):
#     """Returns a list of user's workouts.

#     This function currently returns random data. You will re-write it in Unit 3.
#     """
#     workouts = []
#     for index in range(random.randint(1, 3)):
#         random_lat_lng_1 = (
#             1 + random.randint(0, 100) / 100,
#             4 + random.randint(0, 100) / 100,
#         )
#         random_lat_lng_2 = (
#             1 + random.randint(0, 100) / 100,
#             4 + random.randint(0, 100) / 100,
#         )
#         workouts.append({
#             'workout_id': f'workout{index+1}',
#             'start_timestamp': '2024-01-01 00:00:00',
#             'end_timestamp': '2024-01-01 00:30:00',
#             'start_lat_lng': random_lat_lng_1,
#             'end_lat_lng': random_lat_lng_2,
#             'distance': random.randint(0, 200) / 10.0,
#             'steps': random.randint(0, 20000),
#             'calories_burned': random.randint(0, 100),
#         })
#     return workouts

def get_user_workouts(user_id):
    """Returns a list of user's workouts from BigQuery."""
    client = bigquery.Client(project="brianrivera26techx25",location="US")

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
            `brianrivera26techx25.ISE.Workouts`  
        WHERE
            UserId = @user_id
    """

    # Running the query with the user_id as a parameter
    query_job = client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    ))

    # Wait for the query to complete and get the results
    results = query_job.result()

    # Process the results into a list of workout dictionaries
    workouts = []
    for row in results:
        workout = {
            'workout_id': row.workout_id,
            'start_timestamp': row.start_timestamp,
            'end_timestamp': row.end_timestamp,
            'start_lat_lng': {
                'lat': row.start_lat,  
                'lng': row.start_lng   
            },
            'end_lat_lng': {
                'lat': row.end_lat,   
                'lng': row.end_lng    
            },
            'distance': row.distance,
            'steps': row.steps,
            'calories_burned': row.calories_burned
        }
        workouts.append(workout)
    
    return workouts


# def get_user_profile(user_id):
#     """Returns information about the given user.

#     This function currently returns random data. You will re-write it in Unit 3.
#     """
#     if user_id not in users:
#         raise ValueError(f'User {user_id} not found.')
#     return users[user_id]

def get_user_profile(user_id):
    """Returns user profile info and friends list from BigQuery."""
    client = bigquery.Client(project="brianrivera26techx25",location="US")


    # Query for user info
    user_query = f"""
        SELECT UserId, Name, Username, ImageUrl, DateOfBirth
        FROM `brianrivera26techx25.ISE.Users`
        WHERE UserId = @user_id
    """
    user_job = client.query(user_query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    ))

    user_result = list(user_job.result())
    if not user_result:
        raise ValueError(f"'{user_id}' was not found.")

    user_row = user_result[0]

    # Query for friends
    friends_query = f"""
        SELECT UserId1, UserId2
        FROM `brianrivera26techx25.ISE.Friends`
        WHERE UserId1 = @user_id OR UserId2 = @user_id
    """
    friends_job = client.query(friends_query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    ))

    friends = set()
    for row in friends_job:
        if row.UserId1 == user_id:
            friends.add(row.UserId2)
        else:
            friends.add(row.UserId1)

    # Return user profile dictionary
    return {
        'full_name': user_row.Name,
        'username': user_row.Username,
        'date_of_birth': str(user_row.DateOfBirth),
        'profile_image': user_row.ImageUrl,
        'friends': list(friends)
    }

def get_user_posts(user_id):
    """
    Returns a list of a user's posts. Some data in a post may not be populated.
    Input: user_id
    Output: A list of posts. Each post is a dictionary with keys user_id, post_id, timestamp, content, and image.

    """
    client = bigquery.Client(project="brianrivera26techx25",location="US")

    query = f"""
        SELECT
            PostId AS post_id,
            AuthorId AS user_id,
            Timestamp AS timestamp,
            Content AS content,
            ImageUrl AS image
        FROM
            `brianrivera26techx25.ISE.Posts`  
        WHERE
            AuthorId = @user_id
    """

    # Running the query with the user_id as a parameter
    query_job = client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    ))


    # Wait for the query to complete and get the results
    results = query_job.result()
    posts = []
    for row in results:
        row_post = {
            'user_id': row.user_id,
            'post_id': row.post_id,
            'timestamp': row.timestamp,
            'content': row.content,
            'image': row.image,
        }
        posts.append(row_post)
    return posts
    # }


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
