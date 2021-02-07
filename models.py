from extensions import db

# Current Items in the fridge
class Pictures(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)

    # basic data
    name = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    place = db.Column(db.Integer)
    score = db.Column(db.Float)
    # status
    
    created_at = db.Column(db.DateTime())
    deleted_at = db.Column(db.DateTime())


# Status of Finding recommended recipes
class VotedFor(db.Model):
    __tablename__ = 'votedfor'
    id = db.Column(db.Integer, primary_key=True)

    first = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    second = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    # basic data
    winner = db.Column(db.Integer,db.ForeignKey(Pictures.id),nullable=False)
    
    created_at = db.Column(db.DateTime())
