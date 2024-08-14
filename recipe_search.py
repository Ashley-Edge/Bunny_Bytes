import requests
from dotenv import load_dotenv
import os
import time


# quiz = {"What pasta is shaped like a small bow tie? ": "farfalle"}


# def food_quiz():
#     print("Food Quiz!")
#     for question, answer in quiz.items():
#         user_answer = input(question + "").strip()
#         if user_answer == answer:
#             print("Correct! You may now use the meal planner")
#             return True
#         else:
#             print(f"That is wrong. The correct answer is {answer}")
#             print()
#             print(" /)  /) ~   ┏━━━━━━━━━━━━━━━━━━━━┓")
#             print("(˶>_<˶)  ~  ♡ No dinner for you  ♡")
#             print(" /づづ   ~   ┗━━━━━━━━━━━━━━━━━━━━┛")
#             print("-----------------------------------------------------------------------------------------------------------")
#             no_recipe_sound.play()  # Play no recipe sound
#             time.sleep(1)
#             return False


# Set environment variable to suppress the Pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# Initialize Pygame and Pygame mixer
pygame.init()
pygame.mixer.init()


start_sound = pygame.mixer.Sound('sound/start.wav')
new_recipe_sound = pygame.mixer.Sound('sound/new_recipe.wav')
duplicate_recipe_sound = pygame.mixer.Sound('sound/duplicate_recipe.wav')
no_recipe_sound = pygame.mixer.Sound('sound/no_recipe.wav')

print()
print(" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━┓")
print("( ^_^ ) ~  ♡   Bunny Bytes   ♡")
print(" /づづ    ~ ┗━━━━━━━━━━━━━━━━━┛")
print()
# Play sound at the start of the script
start_sound.play()
load_dotenv()


def recipe_search(ingredient):
    app_id = os.getenv('EDAMAM_APP_ID')
    app_key = os.getenv('EDAMAM_APP_KEY')
    result = requests.get(f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}')
    data = result.json()
    return data['hits']


def read_existing_recipes(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r') as file:
        # Stripping any extra spaces or newline characters from the stored URLs
        existing_urls = {line.split('URL: ')[1].strip() for line in file if line.startswith('   URL:')}
    return existing_urls


def format_recipe(recipe_name, recipe_url, calories_per_serving, servings, ingredients):
    return (
        f"\nRecipe: {recipe_name}\n"
        f"   URL: {recipe_url}\n"
        f"   Calories: {calories_per_serving}\n"
        f"   Servings: {servings}\n"
        f"   Ingredients:\n{ingredients}\n"
        "-----------------------------------------------------------------------------------------------------------"  # Separator line
        ""
    )


def get_recipes():
    print()
    ingredient = input('What ingredients do you want to use?: ')
    while not ingredient:
        ingredient = input('You must enter at least one or more ingredients. Try again: ')

    calories_ask = None
    while calories_ask is None:
        try:
            calories_ask = int(input("Maximum calories per serving: "))
        except ValueError:
            print("Invalid input. Please enter a number for calories.")

    limit = None
    while limit is None:
        try:
            limit = int(input('How many recipes do you want to see?: '))
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of recipes.")

    recipes = recipe_search(ingredient)

    if not recipes:
        print()
        print(" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"(˶>_<˶)  ~  ♡ No recipes found for your ingredients !!!!  ♡")
        print(" /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("-----------------------------------------------------------------------------------------------------------")
        no_recipe_sound.play()  # Play no recipe sound
        time.sleep(1)
        return

    existing_urls = read_existing_recipes('recipes.txt')
    found_recipe = False
    new_recipe_found = False  # Flag to track if a new recipe was found

    with open('recipes.txt', 'a') as file:
        for num, recipe_data in enumerate(recipes[:limit]):
            recipe = recipe_data['recipe']
            recipe_name = recipe['label']
            recipe_url = recipe['url']
            total_calories = recipe['calories']
            servings = recipe.get('yield', 1)  # Default to 1 serving if not provided
            calories_per_serving = round(total_calories / servings)  # Roundup the number
            servings = int(servings)  # Ensure servings is an integer
            ingredients_list = recipe['ingredientLines']
            ingredients = "\n".join(f"      - {line}" for line in ingredients_list)  # format ingredients in a list

            # print(f"DEBUG: Checking recipe - {recipe_name} with {calories_per_serving} calories per serving")  # Debug line

            if calories_per_serving <= calories_ask:
                found_recipe = True
                new_recipe_found = True

                formatted_recipe = format_recipe(recipe_name, recipe_url, calories_per_serving, servings, ingredients)

                if recipe_url in existing_urls:
                    print()
                    print(" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
                    print(f"( ^_^ )  ~ ♡  You have seen this recipe before ♡")
                    print(" /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
                    print(formatted_recipe)
                    # print(format_recipe(recipe_name, recipe_url, calories_per_serving, servings, ingredients))
                    duplicate_recipe_sound.play()  # Play duplicate sound
                    time.sleep(1)
                    continue

                print()
                print(" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━┓")
                print(f"(˶♡_♡˶)  ~ ♡  * New Recipe! * ♡")
                print(" /づづ    ~ ┗━━━━━━━━━━━━━━━━━━┛")
                print(formatted_recipe)  # Print the new recipe
                new_recipe_sound.play()  # Play new recipe sound
                time.sleep(1)

                file.write(formatted_recipe)  # Write the new recipe to the file
                existing_urls.add(recipe_url)

        if new_recipe_found:
            print("** All new recipes have been added to recipes.txt **")
            print("-----------------------------------------------------------------------------------------------------------")

    if not found_recipe:
        print()
        print(" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"(˶>_<˶) ~ ♡  No recipes under {calories_ask} calories are available !!!! ♡")
        print(" /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("-----------------------------------------------------------------------------------------------------------")
        no_recipe_sound.play()  # Play no recipe sound
        time.sleep(1)


# if food_quiz():
#     get_recipes()
get_recipes()
print("♡ Developed Ashley Edge. Special thanks to my GCHQ EDAMAM-team3, where we initially developed this app 2024 ♡")
print("-----------------------------------------------------------------------------------------------------------")
