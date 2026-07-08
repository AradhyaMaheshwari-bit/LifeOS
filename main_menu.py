from utils.validation import validate_menu_choice
from modules.study import study_menu
from modules.workout import workout_menu
from modules.meals import meals_menu
from modules.sleep import sleep_menu
from modules.walks import dog_walk_menu
from modules.report import reports_menu

menu_actions = {
    "1": study_menu,
    "2": workout_menu,
    "3": meals_menu,
    "4": sleep_menu,
    "5": dog_walk_menu,
    "6": reports_menu,
}

def print_main_menu():
    print("\n========== LifeOS ==========")
    print("1. Study")
    print("2. Workout")
    print("3. Meals")
    print("4. Sleep")
    print("5. Dog Walk")
    print("6. Daily Report")
    print("7. Exit")

def main_menu():
    while True:
        print_main_menu()

        choice = input("\nChoose an option: ")

        if not validate_menu_choice(choice):
            print("Please enter a valid choice (1-9).")
            continue
        if choice == "7":
            print("\nGoodbye!")
            break
        menu_actions[choice]()
