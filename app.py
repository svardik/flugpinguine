from flask import Flask
from extensions import db
from backend import backend
from views import views

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(backend)
    app.register_blueprint(views)
    db.init_app(app)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run()
