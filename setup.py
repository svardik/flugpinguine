from flask import Flask

from flask_sqlalchemy import SQLAlchemy

import os, csv
import json
from datetime import datetime
from collections import Counter
from app import create_app, db

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    try:
        db.drop_all()
    except:
        print('No DB found')

    print('\nInitializing new DB')
    db.create_all()
    print('--- DB initialized ---')