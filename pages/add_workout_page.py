from data_fetcher import get_available_exercises
from modules import display_exercise_card, display_exercises_list

exercises = get_available_exercises()

display_exercises_list(exercises)