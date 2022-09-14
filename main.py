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
            'user' : self.user
        }
# db.create_all()
    

class RegistrationForm(FlaskForm):
    name = StringField('username',                  validators =[DataRequired()])
    email = StringField('Email',                    validators=[DataRequired(),Email()])
    password1 = PasswordField('Password',           validators = [DataRequired()])
    password2 = PasswordField('Confirm Password',   validators = [DataRequired(),EqualTo('password1')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',                    validators=[DataRequired(), Email()])
    password = PasswordField('Password',            validators=[DataRequired()])
    remember = BooleanField('Remember Me',          default = False)
    submit = SubmitField('Login')

class BOOK_TICKET(Resource):
    
    def get(self):
        id = current_user.id
        tickets = Theatre.query.filter_by(user = id).all()
        
        for idx in range(len(tickets)):
            tickets[idx] = tickets[idx]._asdict()
            theatre_details = Theatre.query.filter_by(id = tickets[idx]['Theatre_details']).first()
            if not theatre_details:
                continue
            for detail in theatre_details._asdict().keys():
                if detail == 'tickets':continue
                if detail == 'date':continue
                if detail == 'price':continue
                #     tickets[idx][detail] = str(ticket_details._asdict()[detail].date()).split(' ')[0]
                # else:
                tickets[idx][detail] = theatre_details._asdict()[detail]
        print(tickets)
        return jsonify(tickets)
        
    
    def put(self):
        args = request.get_json()
        ticket = Movie(theatre_id = args['id'], tickets = args['ticket'], price = args['price'], user = current_user.id)
        theatre = Theatre.query.get(args['id'])
        theatre.tickets -= args['ticket']
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({'message': 'Ticket Booked'})
    
class ADD_THEATRE_API(Resource):
    def put(self):
        data = request.get_json()
        theatre = Theatre(theatre_name = data['theatre_name'], district = data['theatre_district'], state = data['theatre_state'])

        db.session.add(theatre)
        db.session.commit()
        print("Successfully")

        return {'message': 'Theatre added successfully'}, 201   
    
class SEARCH_MOVIE(Resource):
    def get(self):
        args = request.args
        if args['date'] != '':
            date = parser.parse(args['date'])
        else:
            date = ''
        
        theatre = Theatre.query.all()
        print(theatre)
        if args['theatre_name'] != ' ':
            theatre = list(map(lambda x: x, filter(lambda x: x.from_.lower() == args['theatre_name'].lower(), theatre)))
        if args['movie_name'] != ' ':
            theatre = list(map(lambda x: x, filter(lambda x: x.to_.lower() == args['movie_name'].lower(), theatre)))
        if date != '':
            theatre = list(map(lambda x: x, filter(lambda x: x.date == date, theatre)))
        print(theatre)
        for idx in range(len(theatre)):
            theatre[idx] = theatre[idx]._asdict()
        return jsonify(theatre)
        
class ADD_MOVIE_API(Resource):
    
    def put(self):
        data = request.get_json()
        date = parser.parse(data['date']).date()
        movie = Movie(theatre_name = data['theatre_name'], movie_name = data['movie_name'], date = date, time = data['time'], price = data['price'], ticket = 60 )
        db.session.add(movie)
        db.session.commit()
        print("success")
        return {"status": "success", "object": movie._asdict()}

class VIEW_TICKET(Resource):
    
    def get(self):
        args = request.args
        
        print('here', args)
        tickets = Movie.query.filter_by(flight_id = args['id']).all()
        for idx in range(len(tickets)):
            tickets[idx] = tickets[idx]._asdict()
            theatre_details = Theatre.query.filter_by(id = tickets[idx]['Theatre_id']).first()
            print('\n' * 10)
            print(theatre_details)
            print('\n' * 10)
            if not theatre_details:
                continue
            for detail in theatre_details._asdict().keys():
                if detail == 'tickets':continue
                if detail == 'date':continue    
                if detail == 'price':continue
                #     tickets[idx][detail] = str(theatre_details._asdict()[detail].date()).split(' ')[0]
                # else:
                tickets[idx][detail] = theatre_details._asdict()[detail]
            tickets[idx]['booking_name'] = User.query.filter_by(id = tickets[idx]['user']).first().name
        print(tickets)
        return jsonify(tickets)

def auth():
    return current_user.is_authenticated
    
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/')
@app.route('/index')
def index():
    if auth():
        return render_template('index.html', title = "Home", user = current_user)
    return redirect(url_for('login'))

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name =form.name.data, email = form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/admin_login', methods = ['POST','GET'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data) and user.email == "admin@admin.com":
            login_user(user, remember = form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials')
    return render_template('admin-login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('index'))
        flash('Invalid email address or Password.')    
    return render_template('login.html', form=form)

@app.route('/add_movie')
def add_movie():
    if current_user.email == "admin@admin.com":
        return render_template('add_movie.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_theatre')
def add_theatre():
    if current_user.email == "admin@admin.com":
        return render_template('add_theatre.html')
    return redirect(url_for('index'))

@app.route('/view')
def view():
    if current_user.email == "admin@admin.com":
        return render_template('view.html')
    return redirect(url_for('index'))


api.add_resource(ADD_THEATRE_API,'/add_theatre')
api.add_resource(ADD_MOVIE_API, '/add_movie')
api.add_resource(SEARCH_MOVIE, '/search')
api.add_resource(BOOK_TICKET, '/book')
api.add_resource(VIEW_TICKET, '/tickets')

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0')