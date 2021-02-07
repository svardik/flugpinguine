from datetime import datetime
from flask import Flask, request, render_template, redirect,url_for, Blueprint, flash
from werkzeug.utils import secure_filename
import os
from extensions import db
from models import Pictures,VotedFor
from PIL import Image
from algorithm import determine_score

#from recipe_algo import get_potential_recipes,check_ingr_update

upload_folder = 'files'
backend = Blueprint('backend', __name__)

# # GET ACTIVE ITEMS FORM INVENTORY
# def get_current_inventory():
#     return InventoryItems.query.filter_by(deleted_at=None).all()


# # FIND RECIPES FROM INVENTORY
# def get_recipes_from_inventory():
#     recipes = get_potential_recipes()
#     return recipes


# # GET RECIPE AND INGREDIENTS DETAIL
# def get_recipe_detail(_id):
#     recipe_object = Recipe.query.filter_by(id=_id).first_or_404()
#     ingredients = db.session.query(RecipeIngredients, Ingredient).filter_by(recipe_id=_id).outerjoin(
#         RecipeIngredients, Ingredient.id == RecipeIngredients.ingredient_id).all()
#     return {'recipe':recipe_object,'ingredients':ingredients}


# # update recipe matching object when item is added or deleted by the user
# def update_recipe_matching():
#     rm = RecipeMatching.query.order_by(RecipeMatching.id.desc()).first()
#     if rm:
#         rm.ingredients_changed_at = datetime.now()
#         db.session.commit()


# # --- ENDPOINTS FOR ADDING AND DELETING ITEMS ---
# # ADD NEW ITEM - html form for data transfer
# @backend.route('/picture/new', methods=["POST"])
# def new_inventory():
#     if request.form and request.form['new_ingredient']:
#         new_ingredient_name = request.form['new_ingredient']
        
#         # add item
#         item = InventoryItems(name=new_ingredient_name)
#         db.session.add(item)
#         db.session.commit()

#         # update matching status
#         update_recipe_matching()

#         return redirect(url_for('views.index'))


# # DELETE ITEM - json for data transfer
# @backend.route('/inventory/delete', methods=["DELETE"])
# def delete_inventory():
#     if request.json and request.json['delete_ingredient_id']:
#         delete_ingredient_id = request.json['delete_ingredient_id']

#         # delete item
#         item = InventoryItems.query.filter_by(id=delete_ingredient_id).first()
#         item.deleted_at = datetime.now()
#         db.session.commit()

#         # update matching status
#         update_recipe_matching()
    
#         return {"success":True}

ALLOWED_EXTENSIONS = ['jpg','jpeg','png']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@backend.route('/upload_api', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files or 'name' not in request.form:
            flash('No file part')
            redirect(url_for('views.index'))
        file = request.files['file']
        name = request.form['name']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or name == '':
            flash('No selected file')
            redirect(url_for('views.index'))
        if file and allowed_file(file.filename):
            #try:
            # get last id
            p_new = Pictures(name=name)
            db.session.add(p_new)
            db.session.commit()
            
            image = Image.open(request.files['file'].stream).convert("RGBA")
            
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(THIS_FOLDER, "static/files/"+str(p_new.id)+'.jpg')

            new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
            new_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
            new_image.convert('RGB').save(my_file, "JPEG")  # Save as JPEG

            p_new.image_url = "files/"+str(p_new.id)+'.jpg'
            db.session.commit()      


            #except:
            #    flash("wrong format")
            #    return redirect(url_for('views.index'))

            
            flash('File was saved')
            return redirect(url_for('views.index'))
    return redirect(url_for('views.index'))

@backend.route('/voting_api', methods=['GET'])
def voting():
    if "first" in request.args and "second" in request.args and "winner" in request.args:
        first_id = request.args["first"]
        second_id = request.args["second"]
        winner_id = request.args["winner"]
        vf = VotedFor(first=first_id,second=second_id,winner=winner_id)
        db.session.add(vf)
        db.session.commit()
        determine_score()
        print(winner_id)
    return redirect(url_for('views.voting'))
