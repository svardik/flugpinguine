from flask import Flask, request, render_template, abort, Blueprint, session, redirect, url_for
from functools import wraps
from extensions import db
from models import Pictures,Users
from algorithm import get_two_pictures
import datetime

views = Blueprint('views', __name__)
deadline = datetime.datetime(2021,2,22,5,30)
deadline_voting = datetime.datetime(2021,2,23,20,00)
deadline_leaderboard = datetime.datetime(2021,2,23,20,30)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' in session and session['authenticated']:
            return f(*args, **kwargs)
        return redirect(url_for('views.login', next=request.url))
    return decorated_function


# Homepage for items input
@views.route('/')
def index():
    return render_template('index.html')

# Page to view recommended recipes
@views.route('/leaderboard')
def leaderboard():
    if datetime.datetime.now() < deadline_leaderboard:
        return render_template('leaderboardhidden.html')
    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])
    leaderboard = db.session.query(Pictures,Users).select_from(Pictures).join(Users).filter(Pictures.active==True).order_by(Pictures.place).paginate(per_page=9,page=page,error_out=True)
    return render_template('leaderboard.html', leaderboard=leaderboard,page=page)

# Page to view recommended recipes
@views.route('/upload')
@login_required
def upload():
    if datetime.datetime.now() > deadline:
        return render_template('uploadabgelaufen.html')
    return render_template('upload.html')

# Page to view recommended recipes
@views.route('/voting')
@login_required
def voting():
    if datetime.datetime.now() > deadline_voting:
        return render_template('votingabgelaufen.html')
    pictures = get_two_pictures()
    if pictures:
        return render_template('voting.html',picture1=pictures[0],picture2=pictures[1])
    return render_template('voting.html',picture1=None)

# Page to view details of a certain recipe
@views.route('/picture/<_id>')
def picture_detail(_id):
    picture = db.session.query(Pictures,Users).select_from(Pictures).join(Users).filter(Pictures.id == _id).first()
    return render_template('picture_detail.html', picture=picture)

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/register')
def register():
    return render_template('register.html')


@views.route('/password_flash', methods=['GET'])
def password_flash(password):
    return render_template('password.html',password=password)

