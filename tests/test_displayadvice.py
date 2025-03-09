import unittest
from unittest.mock import patch
import streamlit as st
from modules import display_genai_advice


class TestDisplayGenAiAdvice(unittest.TestCase):

    def setUp(self):
        """Set up test data for AI advice."""
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
    def test_display_genai_advice(self, mock_image, mock_write, mock_markdown, mock_header):
        """Tests if AI advice is displayed correctly without errors."""

        
        display_genai_advice(self.test_advice["timestamp"], self.test_advice["content"], self.test_advice["image"])

        
        mock_header.assert_called_with("🤖 AI-Generated Advice")

        
        mock_markdown.assert_called_with(f"**Date:** {self.test_advice['timestamp']}")

        
        mock_write.assert_called_with(self.test_advice["content"])

        
        mock_image.assert_called_with(self.test_advice["image"], caption="Stay motivated!", use_container_width=True)

    @patch('streamlit.image')
    def test_display_genai_advice_no_image(self, mock_image):
        """Tests if AI advice works correctly when no image is provided."""

        
        display_genai_advice(self.test_advice["timestamp"], self.test_advice["content"], None)

        
        mock_image.assert_not_called()


if __name__ == "__main__":
    unittest.main()
