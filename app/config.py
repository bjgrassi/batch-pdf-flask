import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'app\\uploads'
    STATIC_FOLDER = 'app\\uploads\\static'