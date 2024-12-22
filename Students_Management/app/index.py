from flask import flash, render_template, request, redirect, jsonify
import dao
from app import app, login, db
from flask_login import login_user, logout_user
from app.dao import get_user_by_id
from app.models import UserRole, Student, Class, Score, ScoreType


@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    student_id = data['student_id']
    score_type = data['score_type']
    score = float(data['score'])

    score_type_obj = ScoreType.query.filter_by(name=score_type).first()
    new_score = Score(student_id=student_id, score_type_id=score_type_obj.id, so_diem=score)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/edit_score', methods=['POST'])
def edit_score():
    data = request.json
    student_id = data['student_id']
    score_type = data['score_type']
    old_score = float(data['old_score'])
    new_score = float(data['new_score'])

    score_type_obj = ScoreType.query.filter_by(name=score_type).first()
    score_obj = Score.query.filter_by(student_id=student_id, score_type_id=score_type_obj.id, so_diem=old_score).first()
    if score_obj:
        score_obj.so_diem = new_score
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/delete_score', methods=['POST'])
def delete_score():
    data = request.json
    student_id = data['student_id']
    score_type = data['score_type']
    score = float(data['score'])

    score_type_obj = ScoreType.query.filter_by(name=score_type).first()
    score_obj = Score.query.filter_by(student_id=student_id, score_type_id=score_type_obj.id, so_diem=score).first()
    if score_obj:
        db.session.delete(score_obj)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/")
def index():
    page = request.args.get('page', 1)
    page_size = app.config.get('PAGE_SIZE', 8)
    return render_template('index.html', pages=page_size)


@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/')  # dieu huong ve trang chu
    return render_template('login.html')


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        # Đăng nhập người dùng nếu mật khẩu đúng
        login_user(u)
    else:
        # Nếu thông tin đăng nhập sai, hiển thị thông báo lỗi
        flash("Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin đăng nhập.", "danger")
    return redirect('/admin')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@app.route("/register")
def register_process():
    return render_template('register.html')


@app.route("/tiepnhanhocsinh")
def tiepnhanhocsinh_process():
    return render_template('tiepnhanhocsinh.html')


@app.route("/dieuchinhlop")
def dieuchinhlop_process():
    return render_template('dieuchinhlop.html')


@app.route("/tracuuhocsinh")
def tracuuhocsinh_process():
    return render_template('tracuuhocsinh.html')


@app.route("/quanlymonhoc")
def qlmonhoc_process():
    return render_template('quanlymonhoc.html')


@app.route("/quanlydiem")
def qldiem_process():
    return render_template('quanlydiem.html')


@app.route("/quydinh")
def quydinh_process():
    return render_template('quydinh.html')


@app.route("/tongket")
def tongket_process():
    return render_template('tongket.html')


if __name__ == '__main__':
    from app import admin  # chạy trang admin flask

    app.run(debug=True, port=5001)  # Thay port mặc định (5000) thành 5001
