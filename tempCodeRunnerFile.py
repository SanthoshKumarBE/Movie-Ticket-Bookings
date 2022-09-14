from dateutil import parser
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model

from werkzeug.security import generate_password_hash, check_password_hash


from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo

app                                     = Flask(__name__)
app.secret_key                          = "Prakash Presidio Project"
app.config['TEMPLATES_AUTO_RELOAD']     = True

api                                     = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///db.sqlite'
db                                      = SQLAlchemy(app)
login_manager                           = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  name          = db.Column(db.String(50))
  email         = db.Column(db.String(150), unique = True, index = True)
  password_hash = db.Column(db.String(150))
  joined_at     = db.Column(db.DateTime(), default = datetime.utcnow, index = True)

  def set_password(self, password):
        self.password_hash = generate_password_hash(password)

  def check_password(self,password):
      return check_password_hash(self.password_hash,password)
  @classmethod
  def get(self, id):
    return self.query.get(id)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_name = db.Column(db.String(120))
    district = db.Column(db.String(120))
    state = db.Column(db.String(120))
    
    # def __repr__(self) :
    #     return f'Flight-{self.id} {self.from_}->{self.to_} on {self.date} at {self.time}'
    
    def _asdict(self):
        return {
            'id': self.id,
            'theatre_name' : self.theatre_name,
            'district' : self.district,
            'state' : self.state
        }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    theatre_name = db.Column(db.String(120))
    movie_name = db.Column(db.String(120))
    date = db.Column(db.DateTime())
    time = db.Column(db.String(120))
    price = db.Column(db.Integer)
    ticket = db.Column(db.Integer,default=60)
    user = db.Column(db.Integer, db.ForeignKey('user.id')) 
    
    def _asdict(self):
        return {
            'id': self.id,
            'theatre_id': self.theatre_id,
            'theatre_name': self.theatre_name,
            'movie_name' : self.movie_name,
            'date': self.date.strftime('%d-%b-%Y'),
            'time': self.time,
            'price': self.price,
            'ticket': self.ticket,