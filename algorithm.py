from models import Pictures,VotedFor
import random
from extensions import db

def get_two_pictures():
    all_pics = Pictures.query.all()
    return random.sample(all_pics,2)


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
        if games > 3:
            score = win_lost[i][0] / games
        scores_dir[i]=score
    
    sorted_dir = {k: v for k, v in sorted(scores_dir.items(), key=lambda item: item[1])}
    
    places_dir = list(sorted_dir.keys())[::-1]
    out_dir = {}
    for i in range(pictures):
        _id = places_dir[i]
        pc = Pictures.query.filter_by(id=_id).first()
        if(pc is not None):
            pc.place = i+1
            pc.score = scores_dir[_id]
            db.session.commit()
        place = i+1
        out_dir[_id] = place

    
    return out_dir
