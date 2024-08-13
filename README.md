# <ins>Bunny Bytes</ins>

Python Script initially started as the [final group project](https://github.com/Ashley-Edge/Introduction_to_Python/tree/main/Session_6) from the GCHQ - Introduction to Python & Apps course. This version I have continued to work on and improve in my spare time. I really enjoyed this project

### Would You Like To Use My App?:
- Ensure Python and pip are installed.
- Install requirements:
    ```
  pip install -r requirements.txt
  ```
- Create your own [EDAMAM](https://developer.edamam.com/edamam-docs-recipe-api) account 
- Create a `.env` file to store your API ID and KEY.
    ```
    EDAMAM_APP_ID=your_app_id
    EDAMAM_APP_KEY=your_app_key
  ```
- Add the `.env` to a `.gitignore` to ensure `.env` is not committed to your repo if you wish to fork and use this script as a starting point for yor own script.
### Future Improvements I Would Like To Make:
- Adding dietary requirements
- Exclude recipes that include ingredients a user has black listed (They might hate olives)
- Split the text files into a weekly meal plan and shopping list
- Save favorite recipes instead of new-found recipes
- Make the quiz an optional extra
- Expand the quiz, maybe use a second API?
### Starting Up The App
```
 /)  /)  ~ ┏━━━━━━━━━━━━━━━━━┓
( ^_^ ) ~  ♡   Bunny Bytes  ♡
 /づづ    ~ ┗━━━━━━━━━━━━━━━━━┛

What ingredients do you want to use?: tofu
Maximum calories per serving: 300
How many recipes do you want to see?: 1
```
### New Recipe Added
```
 /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━┓
(˶♡_♡˶)  ~ ♡  * New Recipe! * ♡
 /づづ    ~ ┗━━━━━━━━━━━━━━━━━━┛

Recipe: Fried Sriracha Tofu
   URL: https://honestcooking.com/fried-sriracha-tofu/
   Calories: 255
   Servings: 4
   Ingredients:
      - Extra Firm Tofu 13 oz pack
      - Oil to pan fry or grill
-------------------------------------------------------------
** All New recipes have added to recipes.txt **
-------------------------------------------------------------
```
### Recipe Already Saved
```
 /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
( •_• )  ~ ♡  You have seen this recipe before ♡
 /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Recipe: Fried Sriracha Tofu
   URL: https://honestcooking.com/fried-sriracha-tofu/
   Calories: 255
   Servings: 4
   Ingredients:
      - Extra Firm Tofu 13 oz pack
      - Oil to pan fry or grill
--------------------------------------------------------------
```
### No Recipes Found for Given Ingredients
```
 /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
(˶>_<˶) ~   ♡ No recipes found for your ingredients !!!!  ♡
 /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
--------------------------------------------------------------
```
### No Recipes Found with Calorie Limit
```
 /)  /)  ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
(˶>_<˶) ~  ♡ No recipes under 100 calories are available !!!! ♡
 /づづ    ~ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
--------------------------------------------------------------
```
