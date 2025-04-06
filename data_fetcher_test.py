#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import get_genai_advice

class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        """Tests foo."""
        pass

class TestGenAIAdvice(unittest.TestCase):

    @patch("data_fetcher.bigquery.Client")  # Patch the constructor
    @patch("data_fetcher.TextGenerationModel.from_pretrained")
    def test_get_genai_advice_valid_user(self, mock_model, mock_bigquery_client):
        # Mock BigQuery row result
        mock_row = MagicMock()
        mock_row.__getitem__.side_effect = lambda key: {
            "Name": "Remi",
            "Username": "remi_the_rems",
            "DateOfBirth": "1990-01-01"
        }[key]

        # Setup BigQuery client mock
        mock_client_instance = mock_bigquery_client.return_value
        mock_client_instance.query.return_value.result.return_value = [mock_row]

        # Mock Vertex AI response
        mock_model_instance = MagicMock()
        mock_model_instance.predict.return_value.text = "Stay strong and hydrated!"
        mock_model.return_value = mock_model_instance

        # Call the function
        advice = get_genai_advice("user1")

        # Assertions
        self.assertIn("advice_id", advice)
        self.assertIn("timestamp", advice)
        self.assertEqual(advice["content"], "Stay strong and hydrated!")
        self.assertIn("image", advice)  # image could be None or a URL

    @patch("data_fetcher.bigquery.Client")
    def test_get_genai_advice_invalid_user(self, mock_bigquery_client):
        mock_client_instance = mock_bigquery_client.return_value
        mock_client_instance.query.return_value.result.return_value = []

        result = get_genai_advice("invalid_user")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
