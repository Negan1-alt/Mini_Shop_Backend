from models import User
from models import Product

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

    def add(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

class ProductRepository:
    def __init__(self, db):
        self.db = db

    def list(self, search = None):
        query = self.db.query(Product)
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        return query.order_by(Product.id)

    def get(self, product_id:int):
        return self.db.get(Product, product_id)

    def add(self, product):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def save(self, product):
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product):
        self.db.delete(product)
        self.db.commit()
        return {"message" : "product has been deleted"}

    