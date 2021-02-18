from datetime import datetime
from flask import Flask, request, render_template, redirect,url_for, Blueprint, flash, session,abort
from werkzeug.utils import secure_filename
import os
from extensions import db
from models import Pictures,VotedFor, Users
from PIL import Image
from algorithm import determine_score
import bcrypt
import random
import views

upload_folder = 'files'
backend = Blueprint('backend', __name__)

ALLOWED_EXTENSIONS = ['jpg','jpeg','png']
PASSWORD_TEXTS = ('penguin','pingu','fish','antarktis')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_random_string(length):
    sample_letters = 'abcdefghijklmnopqrstuvwxyz '
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str

# returns a tuple of cleartext password and its hash value
def generate_password():
    passwd = random.choice(PASSWORD_TEXTS)+str(random.randint(10,100))
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt)
    return passwd,hashed

def check_pw(name,pw):
    user_in_db = Users.query.filter_by(name=name).first()
    if user_in_db:
        return bcrypt.checkpw(pw.encode('utf-8'), user_in_db.password)
    return False

@backend.route('/upload_api', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files or 'description' not in request.form or 'authenticated' not in session or not session['authenticated']:
            flash('Upload failed!')
            redirect(url_for('views.index'))
        file = request.files['file']
        description = request.form['description']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            redirect(url_for('views.index'))
        if file and allowed_file(file.filename):
            # deactivate old uploads
            old_pictures = Pictures.query.filter_by(user=session['user_id']).all()
            for p in old_pictures:
                p.active = False

            rs = get_random_string(10)
            p_new = Pictures(description=description, user=session['user_id'], active=True, score=0.0)
            db.session.add(p_new)
            db.session.commit()
            
            image = Image.open(request.files['file'].stream).convert("RGBA")
            basewidth = 400

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))

            image = image.resize((basewidth,hsize), Image.ANTIALIAS)

            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(THIS_FOLDER, "static/files/"+str(p_new.id)+'-'+rs+'.jpg')

            new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
            new_image.paste(image, (0, 0), image)            # Paste the image on the background. Go to the links given below for details.
            new_image.convert('RGB').save(my_file, "JPEG")  # Save as JPEG

            p_new.image_url = "files/"+str(p_new.id)+'-'+rs+'.jpg'
            db.session.commit()      
            
            flash('File was saved')
            return redirect(url_for('views.index'))
    return redirect(url_for('views.index'))

@backend.route('/voting_api', methods=['GET'])
def voting():
    if "first" in request.args and "second" in request.args and "winner" in request.args:
        first_id = request.args["first"]
        second_id = request.args["second"]
        winner_id = request.args["winner"]

        check_vf1 = VotedFor.query.filter_by(first=first_id,second=second_id,user=session['user_id']).first()
        check_vf2 = VotedFor.query.filter_by(first=second_id,second=first_id,user=session['user_id']).first()
        if check_vf1 or check_vf2:
            print('already voted')
            return redirect(url_for('views.voting'))
        

        vf = VotedFor(first=first_id,second=second_id,winner=winner_id,user=session['user_id'], created_at=datetime.now())
        db.session.add(vf)
        db.session.commit()
        print(vf.id)
        if vf.id % 50==0:
            determine_score()
    return redirect(url_for('views.voting'))

@backend.route('/register_api', methods=['POST'])
def register():
    if 'name' in request.form:
        name = request.form['name']
        # check if user already exists
        user_in_db = Users.query.filter_by(name=name).first()
        if user_in_db:
            flash('Es gibt bereits einen Nutzer mit diesem Namen!')
            return redirect(url_for('views.register'))
        
        pw, hashed_pw = generate_password()

        newUser = Users(name=name, password=hashed_pw)
        db.session.add(newUser)
        db.session.commit()

        session['authenticated']=True
        session['user_id']=newUser.id
        session['user']=name

        flash('Erfolgreich registreirt!')
        return views.password_flash(pw)

    flash('Etwas ist bei der Registrierung schiefgelaufen!')
    return redirect(url_for('views.register'))

@backend.route('/login_api', methods=['POST'])
def login():
    if 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        pw = request.form['password']
        try:
        # check if user already exists
            user_in_db = Users.query.filter_by(name=name).first()

            if not user_in_db:
                flash('Diesen Nutzer gibt es nicht!')
                return redirect(url_for('views.login'))

            if check_pw(name,pw):
                session['authenticated']=True
                session['user_id']=user_in_db.id
                session['user']=name
                flash('Erfolgreich angemeldet!')
                return redirect(url_for('views.index'))
        
        
            flash('Nutzer existiert nicht oder falsches Passwort!')
            return redirect(url_for('views.login'))
        except Exception as e:
            return e
        
    
    flash('Etwas ist bei der Anmeldung schiefgelaufen!')
    return redirect(url_for('views.login'))



@backend.route('/reset_login_api', methods=['GET'])
def reset_login():
    session['user'] = None
    session['authenticated'] = False
    return redirect(url_for('views.login'))

@backend.route('/logout_api', methods=['GET'])
def logout():
    session['user'] = None
    session['authenticated'] = False
    flash('Erfolgreich abgemeldet!')
    return redirect(url_for('views.index'))

@backend.route('/own_picture', methods=['GET'])
def find_own_picture():
    if ('user' in session) and (session['user']) and ('authenticated' in session) and 'user_id' in session and session['user_id']:
        own_picture = Pictures.query.filter_by(user=session['user_id'],active=True).first()
        if own_picture:
            return redirect(url_for('views.picture_detail',_id=own_picture.id))
        else:
            return redirect(url_for('views.upload'))
    abort(404)



