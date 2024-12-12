import enum
import hashlib
from collections.abc import Sequence
from email.policy import default
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy

ma_hs_khoi10 = str(datetime.now().year)[-2:] + "10000"
ma_hs_khoi11 = str(datetime.now().year)[-2:] + "11000"
ma_hs_khoi12 = str(datetime.now().year)[-2:] + "12000"

class UserRole(RoleEnum):
    ADMIN = 1
    HOCSINH = 2
    GIAOVIEN = 3
    NHANVIEN = 4


class SexType(enum.Enum):
    Male = 1
    Female = 2


class Semester(enum.Enum):
    HK1 = 1
    HK2 = 2
    FULL = 3


class StudentState(enum.Enum):
    STUDYING = "danghoc"
    ABSENCE = "baoluu"
    GRADUATED = "datotnghiep"
    QUIT = "nghihoc"

class Account(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    joined_date = Column(DateTime(timezone=True), server_default= func.now())
    # relationship
    user = relationship('User',uselist=False,back_populates='account') # Moi quan he 1 1


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dnwyvuqej/image/upload/v1733499646/default_avatar_uv0h7z.jpg')
    surname = Column(String(30), nullable=False)
    last_name = Column(String(10), nullable=False)
    # , gioiTinh, namSinh, soDienThoai, email, diaChi, queQuan, ghiChu,
    gioiTinh = Column(Enum(SexType), default=SexType.Male)
    ngay_thang_nam_sinh = Column(DateTime)
    phone_number = Column(String(10),default='0972286956',nullable=False)
    email = Column(String(30),default='2410000000quyen@pct.edu.vn',nullable=False)
    address = Column(String(50),default='Tân Phú')
    que_quan = Column(String(15),default='Thái Bình')
    ghi_chu = Column(String(250))
    user_role = Column(Enum(UserRole))

    # quan he 1-1 voi Account
    account_id = Column(Integer,ForeignKey('account.id'))
    account = relationship('Account',uselist=False,back_populates='user')
    __mapper_args__ = {
        "polymorphic_on": "user_role",
    }


# Bảng trung gian mối quan hệ nhiều nhiều giữa học sinh và lớp học
class StudentClassYear(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column("student_id",Integer,ForeignKey("user.id"),nullable=False)
    class_id = Column('class_id',Integer,ForeignKey('class.id'),nullable=False)
    ngay_nhap_hoc = Column(DateTime(timezone=True), default=func.now())
    year = db.Column(db.String(9), nullable=False) # "2023-2024"
    __table_args__ = (
             db.UniqueConstraint('student_id','class_id','year' , name='unique_year_class_student'),
         )

    student = relationship('Student', back_populates='classes_associations')
    class_ = relationship('Class', back_populates='students_association')


# Bảng học sinh (joined table inheritance)
class Student(User):
    num_instances = 0
    __tablename__ = 'student'
    id = Column(ForeignKey('user.id'),primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": UserRole.HOCSINH
    }
    trangThai = Column(Enum(StudentState), default=StudentState.STUDYING)
    ma_hoc_sinh = Column(String(10),nullable=False,unique=True)

    # relationship with class
    classes_associations = relationship('StudentClassYear',back_populates='student')
    classes = association_proxy("classes_associations","class_")

    # relationship with Diem
    diem = relationship('Diem', back_populates='student')

# Bảng lớp học
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    class_grade_id = Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)
    class_grade = relationship('ClassGrade', back_populates="classes")
    students_association = relationship("StudentClassYear", back_populates="class_")
    # si_so = Column(Integer, nullable=False, default=0)  View
    students = association_proxy('students_association','student')


# Bang khoi lop
class ClassGrade(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    classes = relationship('Class', back_populates="class_grade")
    subjects = relationship('Subject', back_populates='class_grade')



# Bảng trung gian giữa điểm và loại điểm
class SubjectGradeType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column('subject_id',Integer,ForeignKey('subject.id'),nullable=False)
    grade_type_id = db.Column('grade_type_id',Integer,ForeignKey('grade_type.id'),nullable=False)
    so_cot_diem = db.Column(db.Integer,default=1)

    # relationship voi loai diem
    subject = relationship('Subject',back_populates='grade_types_association')
    grade_type = relationship('GradeType',back_populates='subjects_association')

    # relationship voi diem danh cho hoc sinh nao
    diem = relationship('Diem',back_populates='subject_grade_type')


# Bảng môn học
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    class_grade_id = Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=False)
    class_grade = relationship('ClassGrade', back_populates="subjects")
    semester_number = db.Column(Enum(Semester), default=Semester.FULL)
    grade_types_association = relationship('SubjectGradeType',back_populates='subject')
    grade_types = association_proxy('grade_types_association','grade_type')

# Bảng loại điểm
class GradeType(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    he_so = db.Column(db.Integer,default=1)
    subjects_association = relationship('SubjectGradeType',back_populates='grade_type')
    subjects = association_proxy('subjects_association', 'subject')

# Moi quan he nhieu nhieu giua hoc sinh va mon hoc
class Diem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer,ForeignKey('student.id'),nullable=False)
    subject_grade_type_id = db.Column(db.Integer,ForeignKey('subject_grade_type.id'),nullable=False)

    so_diem = db.Column(db.Float, nullable=False)
    attempt = db.Column(db.Integer, default=1,nullable=False)
    semester_number = db.Column(Enum(Semester), default=Semester.HK1)
    year = db.Column(db.String(9), nullable=False)  # "2023-2024"

    # relationship voi bang Student va bang MonHoc-LoaiDiem
    student = relationship('Student',back_populates='diem')
    subject_grade_type = relationship('SubjectGradeType',back_populates='diem')
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_grade_type_id', 'attempt', 'semester_number', 'year',
                            name='unique_point_of_a_subject_in_a_semester'),
    )

# Bảng năm học và học kỳ
# class Semester(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     year = db.Column(db.String(9), nullable=False)  # Ví dụ: "2023-2024"
#     semester_number = db.Column(db.Integer, nullable=False)  # Học kỳ 1 hoặc 2
#
#     __table_args__ = (
#         db.UniqueConstraint('year', 'semester_number', name='unique_year_semester'),
#     )


# Bảng điểm
# class Grade(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
#     semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
#     grade_type = db.Column(db.String(50), nullable=False)  # '15_minutes', '45_minutes', 'final'
#     grade_value = db.Column(db.Float, nullable=False)
#     attempt = db.Column(db.Integer, nullable=True)  # Số lần kiểm tra (1, 2, ...)
#
#     student = db.relationship('Student', backref='grades')
#     subject = db.relationship('Subject', backref='grades')
#     semester = db.relationship('Semester', backref='grades')

def create_user(surname,lastname, username,password):
    password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
    new_user = User(surname=surname,last_name=lastname,account=Account(username=username,password=password))
    return new_user

def create_student(surname,lastname,password): #dua vao khoi_lop
    Student.num_instances += 1 # co the bi trung
    ma_hoc_sinh = str(int(ma_hs_khoi10) + Student.num_instances)
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return Student(surname=surname,last_name=lastname,account=Account(username=ma_hoc_sinh,password=password),ma_hoc_sinh=ma_hoc_sinh)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

    ## TEST HOC SINH
        #Student.__table__.create(db.engine, checkfirst=True) # chi tao 1 bang duy nhat cung danh cho xoa bang duy
        #db.session.scalars(select(Student)).all()

        # hs1 = create_student('Messi','Lionel',password='12345')
        # hs2= create_user('Ronaldo','Cristiano','12345')


    ## Test Khoi lop va mon hoc

        # ClassGrade.__table__.create(db.engine, checkfirst=True)
        # Subject.__table__.create(db.engine, checkfirst=True)
        # Class.__table__.create(db.engine,checkfirst=True)
        # grade10 = ClassGrade(name="Khoi 10",
        # subjects = [Subject(name="Toan"), Subject(name='Van'), Subject(name='Anh')], classes = [Class(name='10A1'),
        #                                                                                         Class(name='10B2'),
        #                                                                                         Class(name='10B2'),


    ## Test mon hoc va loai diem
        # Subject.__table__.create(db.engine, checkfirst=True)
        # GradeType.__table__.create(db.engine, checkfirst=True)
        # SubjectGradeType.__table__.create(db.engine, checkfirst=True)

        # so_cot_15p = 3 # Trong 1 ky hoc
        # so_cot_1tiet = 2
        # so_cot_gk = 1
        # so_cot_ck = 1
        #
        # toan10 = Subject(name="Toan10")
        # van10 =  Subject(name='Van10')
        # anh10 =  Subject(name='Anh10')
        #
        # grade10 = ClassGrade(name="Khoi 10",subjects = [toan10,van10,anh10])
        #
        # diem_15p = GradeType(name='Diem 15 phut', he_so = 1)
        # diem_1tiet = GradeType(name='Diem 1 tiet', he_so=2)
        # diem_thi_gk = GradeType(name='Diem thi gk', he_so=3)
        # diem_thi_cuoi_ki = GradeType(name='Diem thi gk', he_so=4)
        #
        # for subject in [toan10,van10,anh10]:
        #     for grade_type in [diem_15p,diem_1tiet,diem_thi_gk,diem_thi_cuoi_ki]:
        #         if grade_type == diem_15p:
        #             db.session.add(SubjectGradeType(subject=subject,grade_type=grade_type,so_cot_diem=so_cot_15p))
        #         elif grade_type == diem_1tiet:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_1tiet))
        #         elif grade_type == diem_thi_gk:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_gk))
        #         elif grade_type == diem_thi_cuoi_ki:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_ck))
        #
        # db.session.commit()




     ## Test hoc sinh , lop hoc , bang trung gian

        # Student.__table__.create(db.engine,checkfirst=True) # tao bang hoc sinh
        # Class.__table__.create(db.engine, checkfirst=True) # tao bang lop hoc
        # StudentClassYear.__table__.create(db.engine, checkfirst=True) # tao bang trung gian giua hoc sinh va lop hoc

        # EU = ClassGrade(name='EU')
        # VN = ClassGrade(name='VN')
        # hs1 = create_student('Messi','Lionel',password='12345')
        # hs2= create_student('Ronaldo','Cristiano','12345')
        #
        # hs3 = create_student('Cong','Phuong','33333')
        #
        #
        # lamasia = Class(name='Lamasia')
        # hagl = Class(name='Hoang anh gia lai')
        # EU.classes.append(lamasia)
        # VN.classes.append(hagl)
        #
        #
        # a = StudentClassYear(student=hs1,class_=lamasia,year='2023-2024')
        # b = StudentClassYear(student=hs2,class_=lamasia,year='2023-2024')
        # c = StudentClassYear(student=hs3,class_=hagl,year='2004-2005')
        #
        # db.session.add_all([a,b,c])
        # db.session.commit()

    ## Test Hoc sinh, Diem, Mon hoc

        # Student.__table__.create(db.engine,checkfirst=True)
        # SubjectGradeType.__table__.create(db.engine,checkfirst=True)
        # Diem.__table__.create(db.engine,checkfirst=True)

        # Tao mon hoc cua 1 khoi lop va cac cot diem trong mon hoc do
        so_cot_15p = 3 # Trong 1 ky hoc
        so_cot_1tiet = 2
        so_cot_gk = 1
        so_cot_ck = 1

        toan10 = Subject(name="Toan10")
        van10 =  Subject(name='Van10')
        anh10 =  Subject(name='Anh10')

        grade10 = ClassGrade(name="Khoi 10",subjects = [toan10,van10,anh10])

        diem_15p = GradeType(name='Diem 15 phut', he_so = 1)
        diem_1tiet = GradeType(name='Diem 1 tiet', he_so=2)
        diem_thi_gk = GradeType(name='Diem thi gk', he_so=3)
        diem_thi_cuoi_ki = GradeType(name='Diem thi gk', he_so=4)

        # for subject in [toan10,van10,anh10]:
        #     for grade_type in [diem_15p,diem_1tiet,diem_thi_gk,diem_thi_cuoi_ki]:
        #         if grade_type == diem_15p:
        #             db.session.add(SubjectGradeType(subject=subject,grade_type=grade_type,so_cot_diem=so_cot_15p))
        #         elif grade_type == diem_1tiet:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_1tiet))
        #         elif grade_type == diem_thi_gk:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_gk))
        #         elif grade_type == diem_thi_cuoi_ki:
        #             db.session.add(SubjectGradeType(subject=subject, grade_type=grade_type, so_cot_diem=so_cot_ck))


        #db.session.query(SubjectGradeType,Subject,GradeType).
        # Tao hoc sinh

        hs1 = create_student('Hazard','Eden',password='12345')
        so_cot_diem15p_mon_toan = SubjectGradeType(subject=toan10,grade_type=diem_15p,so_cot_diem=so_cot_15p)
        so_cot_diem1tiet_mon_toan = SubjectGradeType(subject=toan10,grade_type=diem_1tiet,so_cot_diem=so_cot_1tiet)

        diem_toan_15p_hs1_hk1 = Diem(student=hs1,subject_grade_type=so_cot_diem15p_mon_toan,so_diem=10,year="2023-2024")
        diem_toan_1tiet_hs1_hk1 = Diem(student=hs1, subject_grade_type=so_cot_diem1tiet_mon_toan, so_diem=5,
                                     year="2023-2024")
        db.session.add(diem_toan_15p_hs1_hk1)
        db.session.add(diem_toan_1tiet_hs1_hk1)

        db.session.commit()

        for diem in hs1.diem:
            print(diem.student.surname,diem.student.last_name,diem.so_diem, diem.subject_grade_type.subject.name, diem.subject_grade_type.grade_type.name)


        # Note
        # Xong diem cho hoc sinh trong tung mon hoc, mon hoc thuoc khoi lop nao, hoc sinh thuoc lop nao.
        # Thiet ke den giao dien xu ly va charJS dua code len
        # Truoc khi bat dau lam thi xoa het du lieu de tranh bi trung 



        #Note
        # Xong Student, User, Account, ClassGrade, Subject DONE
        # Thiet ke hoc sinh,lop, su dung association proxy DONE

        # Tiep tuc thiet ke cac actor khac


        # Thu sql select


        # NOTE: Thiet ke bang hoc sinh_lop_namhoc
        #      - test thu luu tru du lieu
        #     - test luu theo kieu trong recipe
        #     - Thiet lap moi quan he bang mon hoc va diem
        #     - Thiet lap bang Diem cua hoc sinh
        #     - Test