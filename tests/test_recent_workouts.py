# test_recent_workouts.propertyimport unittest
import streamlit as st
from streamlit.testing.v1 import AppTest
from recent_workouts import display_recent_workouts_page

class TestRecentWorkoutsPage(unittest.TestCase):
    
    def setUp(self):
        """Setup Streamlit app test environment."""
        self.app = AppTest(display_recent_workouts_page)

    def test_page_title_is_displayed(self):
        """Check if the page title appears when loaded."""
        self.app.run()
        self.assertTrue(self.app.text("🐱💪 Muscle Meow: Recent Workouts 🏋️‍♂️"))

    def test_warning_for_empty_user_id(self):
        """Check if a warning appears when user ID is left blank."""
        self.app.run()  # Load the page
        self.app.text_input("🔍 Enter user ID", value="")  # Set input to empty
        self.app.button("🐾Show Recent Workouts🐾").click()  # Click button
        
        self.assertTrue(self.app.warning("⚠️ Please enter a valid user ID."))

    def test_error_for_invalid_user(self):
        """Check if an error appears when an unregistered user is entered."""
        self.app.run()
        self.app.text_input("🔍 Enter user ID", value="invalid_user")
        self.app.button("🐾Show Recent Workouts🐾").click()

        self.assertTrue(self.app.error("User 'invalid_user' not found. Please try again."))

    def test_display_workouts_for_valid_user(self):
        """Check if workouts appear for a registered user."""
        self.app.run()
        self.app.text_input("🔍 Enter user ID", value="user1")
        self.app.button("🐾Show Recent Workouts🐾").click()

        self.assertTrue(self.app.subheader("user1's Recent Workouts Overview"))

if __name__ == "__main__":
    unittest.main()