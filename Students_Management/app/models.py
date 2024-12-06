from email.policy import default
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    GIAOVIEN = 3
    NHANVIEN = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dnwyvuqej/image/upload/v1733499646/default_avatar_uv0h7z.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='admin', username='admin', password=str(hashlib.md5('12345678'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()





