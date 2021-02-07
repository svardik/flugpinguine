from datetime import datetime
from flask import Flask, request, render_template, redirect,url_for, Blueprint, flash
from werkzeug.utils import secure_filename
import os
from extensions import db
from models import Pictures,VotedFor
from PIL import Image
from algorithm import determine_score

upload_folder = 'files'
backend = Blueprint('backend', __name__)

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
            basewidth = 400

            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))

            image = image.resize((basewidth,hsize), Image.ANTIALIAS)

            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(THIS_FOLDER, "static/files/"+str(p_new.id)+'.jpg')

            new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
            new_image.paste(image, (0, 0), image)            # Paste the image on the background. Go to the links given below for details.
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
        #print(winner_id)
    return redirect(url_for('views.voting'))
