from email.policy import default
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from __init__ import db, app
from enum import Enum as RoleEnum
import hashlib

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    GIAOVIEN = 3
    NHANVIEN = 4

class SexType(RoleEnum):
    Male = 1
    Female = 2
    
class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    familyname = Column(String(100), nullable=True)
    phone = Column(String(10), nullable=False, unique=True, default="0764642709")
    email = Column(String(100), nullable=False, unique=True, default="abc@gmail.com")
    sex = Column(Enum(SexType), default=SexType.Male)
    dayofbirth = Column(String(10), nullable=False, default="07/12/2024")
    address = Column(String(100), nullable=True)


# class Category(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    classname = Column(String(5), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    students = relationship('Student', backref='Class', lazy=True)


class Student(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False, default=1)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        
        u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        l1 = Class(classname="10A01", quantity=33)
        l2 = Class(classname="10A02", quantity=33)
        l3 = Class(classname="10A03", quantity=33)
        
        db.session.add_all([l1, l2, l3])
        db.session.commit()

        


        # c1 = Category(name='Điểm')
        # c2 = Category(name='Môn học')
        # c3 = Category(name='Lớp')
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()





