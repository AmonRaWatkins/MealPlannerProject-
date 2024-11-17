import random
import json
from typing import List, Dict


class Meal:
    def __init__(self, name: str, ingredients: List[str], prep_time: int, servings: int, nutrition: Dict[str, int], meal_type: str, dietary_preferences: List[str]):
        # Initialize attributes
        self.name = name
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.servings = servings
        self.nutrition = nutrition  # Calories, protein, carbs, fat
        self.meal_type = meal_type  # Breakfast, Lunch, Dinner
        self.dietary_preferences = [pref.strip().lower() for pref in dietary_preferences]  # Normalize to lowercase

    def __str__(self):
        # Return a string representation of the meal with details
        return (
            f"{self.name} ({self.meal_type})\n"
            f"  Calories: {self.nutrition['calories']} kcal, Protein: {self.nutrition['protein']}g, "
            f"Carbs: {self.nutrition['carbs']}g, Fat: {self.nutrition['fat']}g\n"
            f"  Ingredients: {', '.join(self.ingredients)}"
        )


class User:
    def __init__(self, dietary_preferences: List[str], restrictions: List[str], caloric_needs: int = None):
        self.dietary_preferences = [pref.strip().lower() for pref in dietary_preferences]  
        self.restrictions = [restriction.strip().lower() for restriction in restrictions]  
        self.caloric_needs = caloric_needs
        self.meal_plan = []

    def __str__(self):
        return f"Preferences: {self.dietary_preferences}, Restrictions: {self.restrictions}, Caloric Needs: {self.caloric_needs}"


class MealPlanner:
    def __init__(self):
        self.user = None
        self.meals = self.load_meals_from_json([  # Two paths for json files
            "C:/Users/johnw/OneDrive/Meal Planner Project/meal_planner_recipes.json",
            "C:/Users/johnw/OneDrive/Meal Planner Project/meal_planner_50_meals.json"
        ])

    def load_meals_from_json(self, file_paths):
        meals = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for recipe in data["recipes"]: # open and filter through recipes based on inputs 
                        meal = Meal(
                            name=recipe["name"],
                            ingredients=recipe["ingredients"],
                            prep_time=recipe.get("prep_time", 0),
                            servings=recipe.get("servings", 1),
                            nutrition=recipe["nutrition"],
                            meal_type=recipe["meal_type"].strip().lower(),  # Normalize meal type
                            dietary_preferences=recipe["dietary_preferences"]
                        )
                        meals.append(meal)
            except FileNotFoundError:
                print(f"Error: File not found - {file_path}")
        return meals

    def get_user_preferences(self):
        dietary_preferences = input("Enter dietary preferences (none, vegan, gluten-free): ").split(", ")
        restrictions = input("Enter any food restrictions (e.g., no nuts, no dairy): ").split(", ")
        caloric_needs = input("Enter daily caloric needs (optional, press Enter to skip): ")
        caloric_needs = int(caloric_needs) if caloric_needs else None
        self.user = User(dietary_preferences, restrictions, caloric_needs)
        print(f"User preferences set: {self.user}")

    def generate_weekly_plan(self):
        if not self.user:
            print("User preferences not set. Please set preferences first.")
            return

        self.user.meal_plan = []  # Clear any previous meal plan
        all_meals = random.sample(self.meals, len(self.meals))  # Shuffle meals to maximize variety
        used_meals = set()  # Track globally used meals across the week

        for day in range(7):  # One week
            daily_meals = []
            for meal_type in ["breakfast", "lunch", "dinner"]:
                suitable_meals = [
                    meal for meal in all_meals
                    if meal.meal_type == meal_type and
                    # Check if meal matches dietary preferences or "none" (default allows all)
                    (not self.user.dietary_preferences or "none" in self.user.dietary_preferences or
                     any(pref in meal.dietary_preferences for pref in self.user.dietary_preferences)) and
                    # Ensure meal does not contain restricted ingredients
                    (not self.user.restrictions or
                     all(restriction not in meal.ingredients for restriction in self.user.restrictions)) and
                    meal.name not in used_meals  # Ensure global uniqueness
                ]

                print(f"Checking meals for {meal_type} on day {day + 1}...")
                print(f"Total meals: {len(all_meals)}, Suitable meals: {len(suitable_meals)}")

                if suitable_meals:
                    selected_meal = random.choice(suitable_meals)
                    daily_meals.append(selected_meal)
                    used_meals.add(selected_meal.name)  # Mark this meal as used globally
                else:
                    print(f"Warning: No suitable {meal_type} found for day {day + 1}.")
                    daily_meals.append(None)  # Add placeholder for missing meal

            self.user.meal_plan.append(daily_meals)

        print("Weekly meal plan generated successfully!")

    def display_meal_plan(self):
        if not self.user or not self.user.meal_plan:
            print("Meal plan is empty. Generate a plan first.")
            return

        print("\nGenerated Weekly Meal Plan:")
        for i, day_meals in enumerate(self.user.meal_plan, start=1):
            print(f"Day {i}:")
            for meal in day_meals:
                if meal:
                    print(f" - {meal}")
                else:
                    print(" - No suitable meal found for this slot.")
            print()

    def display_menu(self):
        while True:
            print("\nMeal Planner Menu:")
            print("1. Set Preferences and Restrictions")
            print("2. Generate Weekly Meal Plan")
            print("3. View Meal Plan")
            print("4. Quit")

            choice = input("Choose an option: ")
            if choice == "1":
                self.get_user_preferences()
            elif choice == "2":
                self.generate_weekly_plan()
            elif choice == "3":
                self.display_meal_plan()
            elif choice == "4":
                print("Thank you for using the Meal Planner. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    planner = MealPlanner()
    planner.display_menu()
