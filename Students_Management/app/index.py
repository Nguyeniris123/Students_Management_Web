import math
from flask import render_template, request
import dao
from app import app


@app.route("/")
def index():
    # cates = dao.load_categories()
    # cate_id = request.args.get('category_id')
    # kw = request.args.get('kw')
    page = request.args.get('page', 1)
    page_size = app.config.get('PAGE_SIZE', 8)
    # return render_template('index.html', categories=cates, pages=page_size)
    return render_template('index.html', pages=page_size)

@app.route("/login")
def login_process():
    return render_template('login.html')

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
    app.run(debug=True)
