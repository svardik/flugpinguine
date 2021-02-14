from extensions import db

# Keeps information about users
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    
    password = db.Column(db.String(255))

    # basic data
    created_at = db.Column(db.DateTime())

# Keeps information about uploaded pictures
class Pictures(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)

    # basic data
    user = db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(255))

    active = db.Column(db.Boolean)
    
    place = db.Column(db.Integer)
    score = db.Column(db.Float)
    # status
    created_at = db.Column(db.DateTime())
    deleted_at = db.Column(db.DateTime())


# Keeps information about votes
class VotedFor(db.Model):
    __tablename__ = 'votedfor'
    id = db.Column(db.Integer, primary_key=True)

    first = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    second = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    # basic data
    winner = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    user = db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
    created_at = db.Column(db.DateTime())


