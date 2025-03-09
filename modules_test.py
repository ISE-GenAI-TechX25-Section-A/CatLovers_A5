#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_display_post_renders(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_display_genai_advice_renders(self):
        """Tests if display_genai_advice runs without errors and displays advice correctly."""
        app = AppTest(display_genai_advice, args=("2025-03-07", "Stay strong and keep pushing!", None))
        self.assertFalse(app.exception)  
        self.assertIn("Stay strong and keep pushing!", app.html)  
        self.assertIn("2025-03-07", app.html)  


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
