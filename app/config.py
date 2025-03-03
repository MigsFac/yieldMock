import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = 'Content-Type'
