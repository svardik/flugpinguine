from flask import Flask, request, render_template, abort, Blueprint
#from backend import get_recipes_from_inventory, get_recipe_detail,get_current_inventory
from extensions import db
from models import Pictures
from algorithm import get_two_pictures

views = Blueprint('views', __name__)


# Homepage for items input
@views.route('/')
def index():
    return render_template('index.html')

# Page to view recommended recipes
@views.route('/leaderboard')
def leaderboard():
    leaderboard = Pictures.query.order_by(Pictures.place).all()
    return render_template('leaderboard.html', pictures=leaderboard)

# Page to view recommended recipes
@views.route('/upload')
def upload():
    return render_template('upload.html')

# Page to view recommended recipes
@views.route('/voting')
def voting():
    pictures = get_two_pictures()

    return render_template('voting.html',picture1=pictures[0],picture2=pictures[1])

# Page to view details of a certain recipe
@views.route('/picture/<_id>')
def picture_detail(_id):
    picture = Pictures.query.filter_by(id=_id).first_or_404()
    return render_template('picture_detail.html', picture=picture)

