import pkg_resources
import sys
import os


def dynamic_separator():
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80  # Default to 80 columns if the terminal size is unavailable (pycharm will use this)
    return '-' * terminal_width


# Check if the required dependencies are installed
def check_dependencies():
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [req for req in requirements if req.split('==')[0].lower() not in installed]
    
    if missing:
        print("\n" + dynamic_separator())
        print("\nImportant dependencies are missing")
        print("\nTo install missing dependencies, run:")
        print("     pip install -r requirements.txt\n")
        print(dynamic_separator())
        return False
    return True


if not check_dependencies():
    sys.exit(1)


from dotenv import load_dotenv # type: ignore

def check_env_file():
    if not os.path.exists('.env'):
        print("\n" + dynamic_separator() + "\n")
        print("The .env file is missing.")
        print("\nPlease create a .env file ~ `touch .env`")
        print("\n   Sign up for a free EDAMAM account at https://developer.edamam.com/ to get your unique app ID and key.")
        print("\n   - EDAMAM_APP_ID=your_app_id=<paste your unique app ID here>")
        print("   - EDAMAM_APP_KEY=your_app_key=<paste your unique app key here>")
        print("\n" + dynamic_separator() + "\n")
        return False
    
    load_dotenv()
    app_id = os.getenv('EDAMAM_APP_ID')
    app_key = os.getenv('EDAMAM_APP_KEY')
    
    if not app_id or not app_key:
        print("\n" + dynamic_separator() + "\n")
        print("Your EDAMAM API credentials are missing from the .env file.")
        print("\nPlease ensure your .env file contains:")
        print("\n   - EDAMAM_APP_ID=your_app_id=<paste your unique app ID here>")
        print("   - EDAMAM_APP_KEY=your_app_key=<paste your unique app key here>")
        print("\nTo get these credentials, sign up for a free account at https://developer.edamam.com/")
        print("\n" + dynamic_separator() + "\n")
        return False
    
    return True

# Call this function at the start of your script
if not check_env_file():
    exit(1)


import requests # type: ignore
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
#             print(dynamic_separator())
#             no_recipe_sound.play()  # Play no recipe sound
#             time.sleep(1)
#             return False


# Set environment variable to suppress the Pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame # type: ignore

# Initialize Pygame and Pygame mixer
pygame.init()
pygame.mixer.init()


start_sound = pygame.mixer.Sound('sound/start.wav')
new_recipe_sound = pygame.mixer.Sound('sound/new_recipe.wav')
duplicate_recipe_sound = pygame.mixer.Sound('sound/duplicate_recipe.wav')
no_recipe_sound = pygame.mixer.Sound('sound/no_recipe.wav')

print(
    "\n"
    " /)  /)  ~ ┏━━━━━━━━━━━━━━━━━┓\n"
    "( ^_^ ) ~  ♡   Bunny Bytes   ♡\n"
    " /づづ   ~ ┗━━━━━━━━━━━━━━━━━┛\n"
)
start_sound.play() # Play sound at the start of the script


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
        "\n"
        f"Recipe: {recipe_name}\n"
        f"   URL: {recipe_url}\n"
        f"   Calories: {calories_per_serving}\n"
        f"   Servings: {servings}\n"
        "\n"
        f"   Ingredients:\n{ingredients}\n"
        "\n"
        + dynamic_separator() +  # Separator line
        ""
    )


def get_recipes():
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
    print(dynamic_separator())

    recipes = recipe_search(ingredient)

    if not recipes:
        print(
            "\n"
            f" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"(˶>_<˶) ~  ♡ No recipes found for your ingredients !!!! ♡\n"
            f" /づづ   ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        )
        print(dynamic_separator())
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

                formatted_recipe = format_recipe(recipe_name, recipe_url, calories_per_serving, servings, ingredients)

                if recipe_url in existing_urls:
                    print(
                        "\n"
                        f" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                        f"( ^_^ ) ~  ♡ You have seen this recipe before ♡\n"
                        f" /づづ   ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"                    
                    )
                    print(formatted_recipe)
                    duplicate_recipe_sound.play()  # Play duplicate sound
                    time.sleep(1)
                    continue

                print(
                    "\n"
                    f" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━┓\n"
                    f"(˶♡_♡˶) ~  ♡ * New Recipe! * ♡\n"
                    f" /づづ   ~ ┗━━━━━━━━━━━━━━━━━┛"
                )
                print(formatted_recipe)  # Print the new recipe
                new_recipe_sound.play()  # Play new recipe sound
                time.sleep(1)

                file.write(formatted_recipe)  # Write the new recipe to the file
                existing_urls.add(recipe_url)
                new_recipe_found = True

        if new_recipe_found:
            print("** All new recipes have been added to recipes.txt **")
            print(dynamic_separator())

    if not found_recipe:
        print(
            "\n"
            f" /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"(˶>_<˶) ~  ♡ No recipes under {calories_ask} calories are available !!!! ♡\n"
            f" /づづ   ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        )
        print(dynamic_separator())
        no_recipe_sound.play()  # Play no recipe sound
        time.sleep(1)


# if food_quiz():
#     get_recipes()
get_recipes()
print("♡ Developed Ashley Edge. Special thanks to my GCHQ EDAMAM-team3, where we initially developed this app 2024 ♡")
print(dynamic_separator())
