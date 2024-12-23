import enum
import hashlib
from collections.abc import Sequence
from email.policy import default
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates
from app import db, app
from enum import Enum as RoleEnum, unique
from flask_login import UserMixin

from sqlalchemy.ext.associationproxy import association_proxy
from datetime import date, datetime
import hashlib

ma_hs_khoi10 = str(datetime.now().year)[-2:] + "10000"
ma_hs_khoi11 = str(datetime.now().year)[-2:] + "11000"
ma_hs_khoi12 = str(datetime.now().year)[-2:] + "12000"


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    GIAOVIEN = 3
    NHANVIEN = 4

class Gender(RoleEnum):
    MALE = 1
    FEMALE = 2


class HocKy(RoleEnum):
    HK1 = 1
    HK2 = 2


class KhoiLop(RoleEnum):
    Khoi10 = 1
    Khoi11 = 2
    Khoi12 = 3

class LoaiDiem(RoleEnum):
    diem15p = 1
    diem1tiet = 2
    diemck = 3

class HeSo(RoleEnum):
    heso1 = 1
    heso2= 2
    heso3 = 3

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, default=str(hashlib.md5('1'.encode('utf-8')).hexdigest()))
    user_role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    sex = db.Column(db.Enum(Gender), default=Gender.MALE)  # Giới tính (Enum)
    birth = db.Column(db.Date, nullable=True, default=date(2004, 7, 4))
    address = db.Column(db.String(100), nullable=False, default='123 HCM')  # Địa chỉ
    phone = db.Column(db.String(10), nullable=False, default='0123456789')
    email = db.Column(db.String(100), nullable=False, default='user@example.com')
    avatar = db.Column(db.String(100),
                       default='https://res.cloudinary.com/dnwyvuqej/image/upload/v1733499646/default_avatar_uv0h7z.jpg')


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Tham chiếu đến User


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Tham chiếu đến User
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False, default=1)
    scores = db.relationship('Score', backref='student', lazy=True)

    def __str__(self):
        return f"{self.name} - {self.sex} - {self.birth}"


# Lớp Teacher
class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    department = db.Column(db.String(100), nullable=True)  # Khoa/Bộ môn của giáo viên
    # subject_id = db.Column(db.Integer,db.ForeignKey('subject.id'),nullable=False)
    # subject = relationship('Subject', backref='teachers')

# Lớp Staff
class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Khóa chính tham chiếu từ User
    position = db.Column(db.String(100), nullable=True, default='Nhân viên hành chính')  # Vị trí làm việc


# Bảng lớp học
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_students = db.Column(db.Integer, nullable=False, default=40)
    students = relationship('Student', backref='class', lazy=True)
    class_grade_id = db.Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)

    # class_grade = db.relationship('ClassGrade', backref=db.backref('classes', lazy=True))  # Quan hệ ngược

    def __str__(self):
        return self.name


# Bang khoi lop
class ClassGrade(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(KhoiLop), unique=True, default=KhoiLop.Khoi10)
    classes = relationship('Class', backref='class_grade', lazy=True)
    subjects = relationship('Subject', backref='class_grade', lazy=True)

    def __str__(self):
        return f"{self.name}"


# Bảng năm
class Year(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(9), unique=True, nullable=False, default='2023-2024')  # Ví dụ: "2023-2024"
    semesters = relationship('Semester', backref='year', lazy=True)

    def __str__(self):
        return self.name


# Bảng học kỳ
class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(HocKy), default=HocKy.HK1)  # Học kỳ 1 hoặc 2, hoặc cả 2
    year_id = Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    subjects = relationship('Subject', backref='semester')
    __table_args__ = (
        db.UniqueConstraint('year_id', 'name', name='unique_year_semester'),
    )

    def __str__(self):
        return f"{self.name} - {self.year.name}"

# Bảng môn học
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    class_grade_id = Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)
    semester_id = Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    score_types_association = relationship('SubjectScoreType',back_populates='subject')
    score_types = association_proxy('score_types_association','score_type')

# Bảng loại điểm
class ScoreType(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    he_so = db.Column(db.Integer,default=1)
    subjects_association = relationship('SubjectScoreType',back_populates='score_type')
    subjects = association_proxy('subjects_association', 'subject')

# Bảng môn học - loại điểm
class SubjectScoreType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column('subject_id',Integer,ForeignKey('subject.id'),nullable=False)
    score_type_id = db.Column('score_type_id',Integer,ForeignKey('score_type.id'),nullable=False)
    so_cot_diem = db.Column(db.Integer,default=1)

    # relationship voi loai diem
    subject = relationship('Subject',back_populates='score_types_association')
    score_type = relationship('ScoreType',back_populates='subjects_association')

# Moi quan he nhieu nhieu giua hoc sinh va mon hoc
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer,ForeignKey('student.id'),nullable=False)
    subject_score_type_id = db.Column(db.Integer,ForeignKey('subject_score_type.id'),nullable=False)
    so_diem = db.Column(db.Float, nullable=False)
    attempt = db.Column(db.Integer, default=1,nullable=False)

    # relationship voi bang Student va bang MonHoc-LoaiDiem
    # student from back_ref
    subject_score_type = relationship('SubjectScoreType',backref='score_of_students')
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_score_type_id', 'attempt',name='unique_point_of_a_subject_in_a_semester'),
    )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin1 = Admin(name='admin',
                       username='admin',
                       password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                       user_role=UserRole.ADMIN)
        db.session.add(admin1)

        teacher1 = Teacher(
            name="Nguyen Thi B",
            username="teacher1",
            password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
            user_role=UserRole.GIAOVIEN,
            sex=Gender.FEMALE,
            birth=date(1998, 6, 20),
            address="12 Nguyen Trai, HCMC",
            phone="0908123456",
            email="lan@example.com",
            avatar="https://example.com/avatar.jpg",
        )
        db.session.add(teacher1)

        nhanvien1 = Staff(name='Nguyễn Văn A',
                          username='staff1',
                          password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                          user_role=UserRole.NHANVIEN)
        db.session.add(nhanvien1)

        classgrade10 = ClassGrade(name=KhoiLop.Khoi10)
        classgrade11 = ClassGrade(name=KhoiLop.Khoi11)
        classgrade12 = ClassGrade(name=KhoiLop.Khoi12)
        db.session.add(classgrade10)
        db.session.add(classgrade11)
        db.session.add(classgrade12)

        class10A1 = Class(name='10A1', max_students=40, class_grade=classgrade10)
        db.session.add(class10A1)

        class_instance = Class.query.first()  # Lấy lớp đầu tiên từ bảng `class`

        # Tạo một đối tượng Student
        student1 = Student(
            name="Nguyen Thi Lan",
            username="student1",
            password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
            user_role=UserRole.USER,
            sex=Gender.FEMALE,
            birth=date(2005, 6, 20),
            address="12 Nguyen Trai, HCMC",
            phone="0908123456",
            email="lan@example.com",
            avatar="https://example.com/avatar.jpg",
            class_id=class_instance.id,  # Tham chiếu đến lớp
        )
        db.session.add(student1)

        nam2024 = Year()
        db.session.add(nam2024)

        hocky1_2024 = Semester(year=nam2024)  # mặc định là học kì 1
        db.session.add(hocky1_2024)
        hocky2_2024 = Semester(name=HocKy.HK2, year=nam2024)
        db.session.add(hocky2_2024)

        # # Tao mon hoc cua 1 khoi lop va cac cot diem trong mon hoc do
        # so_cot_15p = 3
        # so_cot_1tiet = 2
        # so_cot_ck = 1

        # Tạo các loai điểm
        diem_15p = ScoreType(name=LoaiDiem.diem15p, he_so=HeSo.heso1)
        diem_1tiet = ScoreType(name=LoaiDiem.diem1tiet, he_so=HeSo.heso2)
        diem_ck = ScoreType(name=LoaiDiem.diemck, he_so=HeSo.heso3)

        # Các loại điểm của môn Toán 10
        toan10_subject_score_types = [
            SubjectScoreType(score_type=diem_15p,so_cot_diem=3),
            SubjectScoreType(score_type=diem_1tiet, so_cot_diem=2),
            SubjectScoreType(score_type=diem_ck, so_cot_diem=1)
        ]

        # Các loại điểm của văn 10
        van10_subject_score_types = [
            SubjectScoreType(score_type=diem_15p, so_cot_diem=3),
            SubjectScoreType(score_type=diem_1tiet, so_cot_diem=2),
            SubjectScoreType(score_type=diem_ck, so_cot_diem=1)
        ]


        # Các loại điểm của anh 10
        anh10_subject_score_types = [
            SubjectScoreType(score_type=diem_15p, so_cot_diem=3),
            SubjectScoreType(score_type=diem_1tiet, so_cot_diem=2),
            SubjectScoreType(score_type=diem_ck, so_cot_diem=1)
        ]

        toan10 = Subject(name="Toan10", semester=hocky1_2024, class_grade=classgrade10, score_types_association=toan10_subject_score_types)
        van10 = Subject(name='Van10', semester=hocky1_2024, class_grade=classgrade10,score_types_association=van10_subject_score_types)
        anh10 = Subject(name='Anh10', semester=hocky1_2024, class_grade=classgrade10,score_types_association=anh10_subject_score_types)

        db.session.add(toan10)
        db.session.add(van10)
        db.session.add(anh10)

        diem_toan_15p_hs1_hk1_2024 = Score(so_diem=7, student=student1, year=nam1, subject=toan10, score_type=diem_15p1)
        diem_toan_1tiet_hs1_hk1_2024 = Score(so_diem=10, student=student1, year=nam1, subject=toan10, score_type=diem_1tiet1)
        diem_toan_ck_hs1_hk1_2024 = Score(so_diem=5, student=student1, year=nam1, subject=toan10, score_type=diem_ck1)

        db.session.add(diem_toan_15p_hs1_hk1_2024)

        db.session.add(diem_toan_1tiet_hs1_hk1_2024)
        db.session.add(diem_toan_ck_hs1_hk1_2024)

        db.session.commit()




