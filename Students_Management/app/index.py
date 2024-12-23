from flask import flash, render_template, request, redirect, jsonify
import dao
from app import app, login, db
from flask_login import login_user, logout_user
from app.dao import get_user_by_id


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

if __name__ == '__main__':
    from app import admin  # chạy trang admin flask

    app.run(debug=True, port=5001)  # Thay port mặc định (5000) thành 5001
