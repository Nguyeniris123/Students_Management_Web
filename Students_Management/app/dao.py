from app.models import Category
from app import app

def load_categories():
    return Category.query.order_by('id').all()
