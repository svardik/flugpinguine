from models import Pictures,VotedFor
from flask import session
import random
from extensions import db
from sqlalchemy.sql import text
import time
import threading

def get_two_pictures():
    result = db.engine.execute(text("""
        select p1.id, p2.id
        from pictures p1, pictures p2
        where p1.id <> p2.id and 
            not exists(
                select * 
                from votedfor v 
                where v.user=%d and ((v.first=p1.id and v.second=p2.id) or (v.first=p2.id and v.second=p1.id)
            )
        );
    """%session['user_id'])).fetchall()
    #print(result)
    if result:
        res = random.choice(result)
        return Pictures.query.filter_by(id=res[0]).first(),Pictures.query.filter_by(id=res[1]).first()
    return None


def determine_score():
    pictures = Pictures.query.count()
    win_lost = [[0,0] for _ in range(pictures+1)]

    votedfor = VotedFor.query.all()
    for v in votedfor:
        if v.first >= 0 and v.second >=0 and v.winner>=0:
            if v.first==v.winner:
                win_lost[v.first][0]+=1
                win_lost[v.second][1]+=1
            else:
                win_lost[v.first][1]+=1
                win_lost[v.second][0]+=1
    scores_dir = {}
    for i in range(len(win_lost)):
        score = 0.0
        games = sum(win_lost[i])
        if games > 5:
            score = win_lost[i][0] / games
        scores_dir[i]=score
    
    sorted_dir = {k: v for k, v in sorted(scores_dir.items(), key=lambda item: item[1])}
    
    places_dir = list(sorted_dir.keys())[::-1]
    out_dir = {}
    
    current_place = 1
    for i in range(pictures):
        _id = places_dir[i]
        pc = Pictures.query.filter_by(id=_id).filter_by(active=True).first()
        if(pc is not None):
            pc.place = current_place
            pc.score = scores_dir[_id]
            db.session.commit()
            current_place+=1
            out_dir[_id] = current_place
    return out_dir


