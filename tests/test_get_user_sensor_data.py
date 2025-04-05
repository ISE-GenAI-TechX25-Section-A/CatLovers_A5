import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import get_user_sensor_data 

"""Run tests: pytest"""
"""test_get_user_sensor_data_multiple_rows written by ChatGPT with slight modifications"""

class TestGetUserSensorData(unittest.TestCase):
    """Tests the get_user_sensor_data function."""
    

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data_multiple_rows(self, mock_bigquery_client):
        # Create multiple mock sensor data rows
        sensor_data_rows = []
        sensor_ids = ["sensor1", "sensor2", "sensor3"]
        timestamps = ["2024-07-29T10:00:00", "2024-07-29T10:05:00", "2024-07-29T10:10:00"]
        values = [123, 4000, 36]

        for sensorID, timestamp, value in zip(sensor_ids, timestamps, values):
            mock_row = MagicMock()
            mock_row.SensorId = sensorID
            mock_row.Timestamp = timestamp
            mock_row.SensorValue = value
            sensor_data_rows.append(mock_row)

        # Create corresponding mock sensor type rows
        sensor_type_rows = []
        names = ["Heart Rate", "Step Count", "Temperature"]
        units = ["bpm", "steps", "Celsius"]

        for sensorID, name, unit in zip(sensor_ids, names, units):
            mock_row = MagicMock()
            mock_row.SensorId = sensorID
            mock_row.Name = name
            mock_row.Units = unit
            sensor_type_rows.append(mock_row)

        # Mock the BigQuery client and its query results
        mock_client_instance = mock_bigquery_client.return_value
        mock_client_instance.query.return_value.result.side_effect = [
            sensor_data_rows,
            sensor_type_rows
        ]

        # Call the function
        result = get_user_sensor_data("user1", "workout1")

        # Define expected output
        expected = [
            {'sensor_type': "Heart Rate", 'timestamp': "2024-07-29T10:00:00", 'data': 123, 'units': "bpm"},
            {'sensor_type': "Step Count", 'timestamp': "2024-07-29T10:05:00", 'data': 4000, 'units': "steps"},
            {'sensor_type': "Temperature", 'timestamp': "2024-07-29T10:10:00", 'data': 36, 'units': "Celsius"}
        ]

        self.assertEqual(result, expected)

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data_no_rows(self, mock_bigquery_client):
        mock_client_instance = mock_bigquery_client.return_value

        mock_sensor_data_query = mock_client_instance.query.return_value
        mock_sensor_data_query.result.return_value = []
        mock_sensor_type_query = mock_client_instance.query.return_value
        mock_sensor_type_query.result.return_value = []


        mock_client_instance.query.side_effect = [mock_sensor_data_query, mock_sensor_type_query]

        result = get_user_sensor_data("user1", "workout1")
        self.assertEqual(result, [])

        

if __name__ == '__main__':
    unittest.main()
