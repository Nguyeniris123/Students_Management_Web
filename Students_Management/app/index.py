import math
from flask import render_template, request
import dao
from app import app


@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    page_size = app.config.get('PAGE_SIZE', 8)
    return render_template('index.html', categories=cates, pages=page_size)

@app.route("/login")
def login_process():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
