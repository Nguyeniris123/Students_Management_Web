from sqlalchemy import func

from app.models import User, Score, ScoreType
from app import app, db
import hashlib

def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username),
                          User.password.__eq__(password))

    # if role:
    #     u = u.filter(User.user_role.__eq__(role))

    return u.first()

def get_user_by_id(id):
    return User.query.get(id)

# Lay ra nhung hoc sinh hoc mon hoc
def get_all_students_average_score(subject_id):
    return db.session.query(Score.student_id,Score.subject_id,(func.sum(Score.so_diem * ScoreType.he_so)/func.sum(ScoreType.he_so)).label('DiemTrungBinh'))\
        .filter(Score.subject_id.__eq__(subject_id)).join(ScoreType,ScoreType.id.__eq__(Score.score_type_id)).group_by(Score.student_id).all()

