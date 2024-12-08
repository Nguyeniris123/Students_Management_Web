from email.policy import default
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
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

# Bảng năm học và học kỳ
class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(9), nullable=False)  # Ví dụ: "2023-2024"
    semester_number = db.Column(db.Integer, nullable=False)  # Học kỳ 1 hoặc 2

    __table_args__ = (
        db.UniqueConstraint('year', 'semester_number', name='unique_year_semester'),
    )

# Bảng lớp học
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Bảng học sinh
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    class_ = db.relationship('Class', backref='students')

# Bảng môn học
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Bảng điểm
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    grade_type = db.Column(db.String(50), nullable=False)  # '15_minutes', '45_minutes', 'final'
    grade_value = db.Column(db.Float, nullable=False)
    attempt = db.Column(db.Integer, nullable=True)  # Số lần kiểm tra (1, 2, ...)

    student = db.relationship('Student', backref='grades')
    subject = db.relationship('Subject', backref='grades')
    semester = db.relationship('Semester', backref='grades')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        u1 = User(name='admin', username='admin', password=str(hashlib.md5('12345678'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        u2 = User(name='giaovien1', username='giaovien1', password=str(hashlib.md5('12345678'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.GIAOVIEN)
        u3 = User(name='nhanvien1', username='nhanvien1', password=str(hashlib.md5('12345678'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.NHANVIEN)

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)


        years = ['2023-2024', '2024-2025']
        for year in years:
            for semester_number in [1, 2]:
                if not Semester.query.filter_by(year=year, semester_number=semester_number).first():
                    db.session.add(Semester(year=year, semester_number=semester_number))
        db.session.commit()
