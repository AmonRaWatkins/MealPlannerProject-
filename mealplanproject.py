from typing import List, Dict
import json

class Meal:
    def __init__(self, name: str, ingredients: List[str], prep_time: int, servings: int, nutrition: Dict[str, int], meal_type: str):
        # Initialize attributes
        self.name = name
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.servings = servings
        self.nutrition = nutrition # Calories, protein, carbs, fat 
        self.meal_type = meal_type # Breakfast, Lunch, Dinner 

    def __str__(self):
        # Return a string representation of the meal
        return f"{self.name} ({self.meal_type}) - {self.servings} servings, {self.prep_time} min prep time"
    
class User:
    def __init__(self, dietary_preferences: List[str], restrictions: List[str], caloric_needs: int = None):
        self.dietary_preferences = dietary_preferences # vegan, low-carb, etc
        self.restrictions = restrictions
        self.caloric_needs = caloric_needs
        self.meal_plan = []

    def __str__(self):
        return f"Preferences: {self.dietary_preferences}, Restrictions: {self.restrictions}, Caloric Needs: {self.caloric_needs}"
    
class MealPlanner:
    def __init__(self):
        self.user = None 
        self.meals = self.load_meals_from_json("C:/Users/johnw/OneDrive/Meal Planner Project/meal_planner_recipes.json") # meal plan recipies will add more in final project 

    def load_meals_from_json(self, file_path):
        meals = []
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for recipe in data["recipes"]:
                    meal = Meal(name=recipe["name"], ingredients=recipe["ingredients"], prep_time=recipe.get("prep_time", 0), servings=recipe.get("servings", 1), nutrition=recipe["nutrition"], meal_type=recipe["meal_type"])
                    meals.append(meal)
        except FileNotFoundError:
            print("Error: file not found.")
        return meals
       
    
    def get_user_preferences(self):
        dietary_preferences = input("Enter dietary preferences (e.g., vegan, gluten-free):").split(", ")
        restrictions = input("Enter any food restrictions (e.g., no nuts, no dairy): ").split(",")
        caloric_needs = input("Enter daily caloric needs (optional, press Enter to skip): ")
        self.user = User(  dietary_preferences, restrictions, caloric_needs)
        print(f"User preferences set: {self.user}")

    def generate_weekly_plan(self):
        if not self.user:
            print("User preferences not set. Please set preferences first. ")
            return
        
        for day in range(7): # One week
            daily_meals = []
            for meal_type in ["breakfast, lunch, dinner"]:
                suitable_meals = [
                    meal for meal in self.meals if meal.meal_type == meal_type and all(pref in meal.nutrition for pref in self.user.dietary_preferences) and all(restriction not in meal.ingredients for restriction in self.user.restrictions)
                ]
                if suitable_meals:
                    daily_meals.append(suitable_meals[0]) #pick first suitable meal
            self.user.meal_plan.append(daily_meals)
        print("Weekly meal plan generated successfully!")
    
    def display_meal_plan(self):
        if not self.user or not self.user.meal_plan:
            print("Meal plan is empty. Generate a plan first. ")
            return
        
        print("\nGenerated Weekly Meal Plan: ")
        for i, day_meals in enumerate(self.user.meal_plan, start=1):
            print(f"Day {i}:")
            for meal in day_meals:
                print(f" -{meal}")
            print()
    
    def search_meals(self, keyword: str):
        results = [meal for meal in self.meals if keyword.lower() in meal.name.lower() or keyword.lower() in "".join(meal.ingredients).lower()]
        if results:
            print("Search Results: ")
            for meal in results:
                print(meal)
        else:
            print("No meals found with the given keyword ")

    def display_menu(self):
        while True:
            print("\nMeal Planner Menu:")
            print("1. Set Preferences and Restrictions")
            print("2. Generate Weekly Meal Plan")
            print("3. Search Meals")
            print("4. View Meal Plan")
            print("5. Quit")

            choice = input("Choose and option: ")
            if choice == "1":
                self.get_user_preferences()
            elif choice == "2":
                self.generate_weekly_plan()
            elif choice == "3":
                keyword = input("Enter a keyword to search for meals: ")
                self.search_meals(keyword)
            elif choice == "4":
                self.display_meal_plan()
            elif choice == "5":
                print("Thank you for using the Meal Planner. Goodbye! ")
                break
            else:
                print("Invalid choice. Please try again. ")


if __name__ == "__main__":
    planner = MealPlanner()
    planner.display_menu()