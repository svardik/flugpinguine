# from extensions import db
# from datetime import datetime
# from models import InventoryItems, Recipe, RecipeIngredients, Ingredient, RecipeMatching, RecipeRecommendation
# from elastic.elastic import search_ingredients, add_ingredient, delete_all_ingredients


# # decides which ingredients match user input items
# def get_ingredients_from_inventory():
#     # find active items in inverntory
#     inventory = InventoryItems.query.filter_by(deleted_at=None).all()

#     # find all recipe ingredients matching active items in the inventory
#     ingredients_in_inventory = set()
#     for item in inventory:
#         for ingreditent_id in search_ingredients(item.name):
#             ingredients_in_inventory.add(ingreditent_id)
#     return ingredients_in_inventory


# # compares own items with ingredients of a recipe and establishes a recommendation score
# def explore_ingredients_of_recipe(recipe_id, ingredients_in_inventory):
#     # get all recipe ingredients
#     recipe_ingredients_list = RecipeIngredients.query.filter_by(
#         recipe_id=recipe_id).all()

#     # find the amount of matching ingredients from inventory
#     matching_ingredients = 0
#     for recipe_ingredient in recipe_ingredients_list:
#         if str(recipe_ingredient.ingredient_id) in ingredients_in_inventory:
#             matching_ingredients += 1
#     # return the matching score
#     return (float(matching_ingredients)/len(recipe_ingredients_list))


# # queries ALL RECIPES and creates score to find out how much ingredients the user has for each recipe
# def find_relevant_recipes(ingredients_in_inventory, min_score):
#     # create recipe matching object
#     rm_id = create_recipematching_db()

#     # find all relevant recipes
#     all_potential_recipes = []

#     all_recipes = Recipe.query.all()
#     for recipe in all_recipes:
#         recipe_score = explore_ingredients_of_recipe(
#             recipe.id, ingredients_in_inventory)
#         # recipe really relevant
#         if recipe_score > min_score:
#             all_potential_recipes.append(
#                 {'obj': recipe, 'score': recipe_score})
#             # save recipe recommendation into DB
#             ro = RecipeRecommendation(recipe_id=recipe.id, score=recipe_score, created_at=datetime.now(), recipe_matching_id=rm_id)
#             db.session.add(ro)
#         db.session.commit()
#     return all_potential_recipes


# # --- DB TOOLS ---
# # returns true if anything has changed since last matching
# def check_ingr_update():
#     rm = RecipeMatching.query.order_by(RecipeMatching.id.desc()).first()
#     # no matching has happened yet or ingredients were updated
#     return bool((not rm) or rm.ingredients_changed_at)

# # returns recipes from last matching (used when no user item was updated to faster show recipe recommendations)
# def get_recipes_from_last_matching():
#     relevant_recipes = []
#     # last matching object
#     rm = RecipeMatching.query.order_by(RecipeMatching.id.desc()).first()
#     for r in rm.recipe_recommendation:
#         recipe_obj = Recipe.query.filter_by(id=r.recipe_id).first()
#         score = r.score
#         relevant_recipes.append({'obj': recipe_obj, 'score': score})
#     return relevant_recipes

# # saves information about current matching into DB
# def create_recipematching_db():
#     rm = RecipeMatching(created_at=datetime.now())
#     db.session.add(rm)
#     db.session.commit()
#     return rm.id

# # saves a recipe
# def relevant_recipe_to_db(recipe_id, score, rm_id):
#     ro = RecipeRecommendation(recipe_id=recipe_id, score=score,
#                               created_at=datetime.now(), recipe_matching_id=rm_id)
#     db.session.add(ro)
#     db.session.commit()


# # --- MOST IMPORTANT FUNCTION ---
# # out: [{'obj':<SQLAlchemy record>, 'score':float},...]
# def get_potential_recipes():
#     # ingredients changed since the last query?
#     if check_ingr_update():
#         # new recipes are matched
#         ingredients_in_inventory = get_ingredients_from_inventory()
#         relevant_recipes = find_relevant_recipes(ingredients_in_inventory, 0.7)
#     else:
#         # recipe recommendations from last matchng are used
#         relevant_recipes = get_recipes_from_last_matching()

#     # recipes are sorted by score
#     relevant_recipes_sorted = sorted(
#         relevant_recipes, key=lambda r: r['score'], reverse=True)
#     return relevant_recipes_sorted
