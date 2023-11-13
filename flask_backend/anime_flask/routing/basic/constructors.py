from anime_flask import app
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_marshmallow import Marshmallow
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token  
from flask_mail import Mail, Message

# Put data file in same path as app file
basedir =  os.path.abspath(os.path.dirname(__file__))
basedir = basedir[:-14]
dataURI = 'sqlite:///' + os.path.join(basedir, 'Data/sqlite/planets.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Data/sqlite/planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # CHange this IRL
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_PASSWORD'] = '21f158aaff91df'
app.config['MAIL_USERNAME'] = '6fede7a320205b'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.secret_key = "MySecretKey1234"
 
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

# Constructor class for database model
class User(db.Model):
    __table_name__ = 'users'
    username = Column(String, unique=True)
    id = Column(Integer, primary_key=True)
    user_watching = Column(Integer)
    user_completed = Column(Integer)
    user_dropped = Column(Integer)
    user_plantowatch = Column(Integer)
    user_days_spent_watching = Column(Float)
    gender = Column(String)
    location = Column(String)
    birth_date = Column(String)
    join_date = Column(String)
    stats_mean_score = Column(Float)
    stats_rewatched = Column(Float)
    stats_episodes = Column(Float)
    email = Column(String, unique=True)
    password = Column(String)
    
class UserSentence(db.Model):
    __table_name__ = 'user_sentence'
    id = Column(Integer, primary_key=True)
    sentence = Column(String)
    
class Planet(db.Model):
    __table_name__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class Reviews(db.Model):
    __table_name__ = 'reviews'
    order = Column(Integer, primary_key=True)
    uid = Column(Integer)
    profile = Column(String)
    anime_uid = Column(Integer)
    text = Column(String)
    score = Column(Float)
    scores = Column(String)
    link = Column(String)
    
class Angular(db.Model):
    __table_name__ = 'angular'
    anime_id = Column(Integer, primary_key = True)
    title = Column(String)
    genre = Column(String)
    season = Column(String)
    image_url = Column(String)
    episodes = Column(Integer)
    score = Column(Integer)
    synopsis = Column(String)
    year = Column(Integer)
    episode_url = Column(String)
    
class DocVec(db.Model):
    __table_name__ = 'Doc2Vec'
    anime_id = Column(Integer, primary_key=True)
    title = Column(String)
    synopsis = Column(String)
    model = Column(String)
class UserSchema(ma.Schema):
    class Meta:
        fields=('id', 'username', 'gender', 'location', 'user_watching', 'user_completed', 'user_dropped', 'user_plantowatch', 'user_days_spent_watching', 'birth_date', 'join_date', 'stats_mean_score', 'stats_rewatched', 'stats_episodes')
class DocVecSchema(ma.Schema):
    class Meta:
        fields=('anime_id', 'title', 'synopsis', 'model')
class ReviewsSchema(ma.Schema):
    class Meta:
        fields=('order', 'uid', 'profile', 'anime_uid', 'text', 'score', 'scores', 'link')
class UserSentenceSchema(ma.Schema):
    class Meta:
        fields=('id', 'sentence')
class PlanetSchema(ma.Schema):
    class Meta:
        fields=('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

class AngularSchema(ma.Schema):
    class Meta:
        fields=('anime_id', 'title', 'episodes', 'score', 'year', 'genre', 'synopsis', 'season', 'image_url', 'episode_url')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
doc2vec_schema = DocVecSchema()
doc2vecs_schema = DocVecSchema(many=True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)
angular_schema = AngularSchema()
reviews_schema = ReviewsSchema(many=True)
review_schema = ReviewsSchema()
angulars_schema = AngularSchema(many=True)
userSentences_schema = UserSentenceSchema(many=True)