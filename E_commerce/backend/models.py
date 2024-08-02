from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Float, CHAR, DateTime

class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(CHAR(255), nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    price = Column(Float)
    description = Column(String(100))
    photos = Column(String)
    reviews = Column(String(25))

class Order(Base):
    __tablename__ = 'orders'
    id = Column(String(100),primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    order_id = Column(String(255),primary_key=True)
    quantity = Column(Integer)
    delivery_date = Column(DateTime)
    order_placed = Column(DateTime)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String(100),primary_key=True)
    payment_method = Column(String(20))
    card_no = Column(String(255),unique=True)
    tokenized_card_no = Column(String(255))
    expiry_date = Column(DateTime)
    card_name = Column(String(30))
