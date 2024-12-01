from email.policy import default
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)


# class Category(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        # c1 = Category(name='Điểm')
        # c2 = Category(name='Môn học')
        # c3 = Category(name='Lớp')
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()





