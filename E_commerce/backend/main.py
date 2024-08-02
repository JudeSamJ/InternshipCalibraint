from database import engine,SessionLocal
from pydantic import BaseModel
from typing import Annotated
from datetime import date
from passlib.hash import bcrypt
import models , os ,random,smtplib
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail , MessageSchema,ConnectionConfig
from dotenv import load_dotenv
from fastapi_mail import FastMail,MessageSchema
from fastapi_mail.errors import ConnectionErrors
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from utils import create_access_token,create_refresh_token,cardno_token
from authentication import get_current_user
from OpenSSL import SSL
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.message import EmailMessage

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session ,Depends(get_db)]

class generateOTP(BaseModel):
    to_mail:str

class userSignup(BaseModel):
    username:str
    password:str
    email:str

class getUser(BaseModel):
    username:str
    password:str
    email:str

class SMSToken(BaseModel):
    token:str

class Phonenumber(BaseModel):
    phonenumber:str

class SMSValidateCode(BaseModel):
    code:str

class SMSMessage(BaseModel):
    message:str

class createProduct(BaseModel):
     name:str
     price:float
     description:str
     photos:str
     reviews:str

class orderProduct(BaseModel):
    name:str
    price:int

class createOrder(orderProduct):
    quantity:int
    delivery_date:date
    order_placed:date

class TokenSchema(BaseModel):
    access_token:str
    refresh_token:str

class paymentRequest(BaseModel):
    card_no:int
    payment_method:str
    expiry_date:date
    card_name:str 

from fastapi import FastAPI

app = FastAPI()
def generate_otp(otp):
    otp=""
    for i in range(6):
        otp += str(random.randint(0,9))
        return otp

@app.post("/generate_otp/",status_code=status.HTTP_201_CREATED)
def create_user(generate:generate_otp ,db: db_dependency):
        otp_gen = models.User(otp=generate.otp)
        db.add(otp_gen)
        db.commit()
        return {"message": "OTP is generated successfully.  "}
        # gen_otp = models.User(otp=tomail.otp)
        # db.add(gen_otp)
        # db.commit()
        return {"message": "OTP is generated"}
   
@app.post("/user_creation/",response_model=userSignup)
def create_user(user:userSignup,db:db_dependency):
    hashed_password = bcrypt.hash(user.password)
    new_user = models.User(id=str(uuid4()),username=user.username,password=hashed_password,email=user.email)
    db.add(new_user)
    db.commit()
def verify_otp(otp):
    if otp == models.User.otp:
        return create_user()
    
@app.post("/user_login/",status_code=status.HTTP_200_OK,response_model=TokenSchema)
def user_login(db:db_dependency,form_data:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter_by(username=form_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect email or Password")
    hashed_pass = user.password
    if not bcrypt.hash(hashed_pass):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Incorrect password please check your pasword'
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email)
    }

@app.get("/get_user_details/",status_code = status.HTTP_200_OK)
def get_user_details(user:getUser = Depends(get_current_user)):
     db_get_details = user
     if db_get_details is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User not found")
     else:
          return db_get_details

@app.post("/products/",status_code=status.HTTP_201_CREATED)
def create_product(product:createProduct ,db: db_dependency):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    return {"Message":"Product is added"}
    
@app.get("/get_product_info/",status_code =status.HTTP_200_OK)
def get_product_details(product_id:int , db:db_dependency):
     db_product_details = db.query(models.Product).filter(models.Product.id == product_id).first()
     if db_product_details is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Product not found")
     else:
          return db_product_details

@app.post("/place-order/",response_model= createOrder)
def place_order(order:createOrder,db:db_dependency, current_user = Depends(get_current_user)):
        db_order = models.Order(order_id=str(uuid4()),id=current_user.id,quantity=order.quantity,delivery_date=order.delivery_date,order_placed=order.order_placed)
        db.add(db_order)
        db.commit()

@app.post("/payment/")
def payment(payment:paymentRequest,db:db_dependency,card_no = cardno_token,payment_option = Depends(get_current_user)):
    db_payment = models.Payment(
        payment_method = payment.payment_method,
        card_no = card_no(payment.card_no),
        card_name = payment.card_name,
        expiry_date = payment.expiry_date
    )
    db.add(db_payment)
    db.commit()

# @app.get("/get_order_details/",status_code = status.HTTP_200_OK)
# def get_order_details(username: str, db: Session):
#     get_details = db.query(models.Order).filter(models.Order.user == username).first()
#     if get_details is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     else:
#         return get_details
