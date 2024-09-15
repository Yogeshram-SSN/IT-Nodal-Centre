from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres.exaadpekttnnxcfiglwt:Adsavvyy123@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SupaUser1(db.Model):
    __tablename__ = 'supa_user1'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and user.password == password:
            return user
        return None

    @classmethod
    def user_exists(cls, username):
        return cls.query.filter_by(username=username).first() is not None

class CompletedScholars(db.Model):
    __tablename__ = 'Completed_Scholars'
    Completion_ID = db.Column(db.Integer, primary_key=True)


class OngoingScholars(db.Model):
    __tablename__ = 'Ongoing_Scholars'
    Scholar_ID = db.Column(db.Integer, primary_key=True)
    Name_of_scholar = db.Column(db.String)
    Register_Number = db.Column(db.String)
    Gender = db.Column(db.String)
    Research_Status = db.Column(db.String)
    Full_time_Part_Time = db.Column(db.String)

class Supervisors(db.Model):
    __tablename__ = 'Supervisors'
    Supervisor_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    ERP_Code = db.Column(db.String)
    Email = db.Column(db.String)
    Gender = db.Column(db.String)
    Designation = db.Column(db.String)
    Supervisor_Recognition_Number = db.Column(db.String)


with app.app_context():
    db.create_all()
    
@app.route("/")
def login():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    user = SupaUser1.authenticate(username, password)
    if user:
        session['user_id'] = user.user_id
        return redirect(url_for('dashboard'))
    else:
        return render_template('home.html', error='Invalid username or password')

@app.route("/register", methods=['GET', 'POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    
    if SupaUser1.user_exists(username):
        return render_template('home.html', error='Username already exists')
    else:
        try:
            new_user = SupaUser1(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.user_id
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            return render_template('home.html', error='An error occurred while registering')

@app.route('/dashboard')
def dashboard():
    completed_scholars_count = CompletedScholars.query.count()
    print(completed_scholars_count)
    ongoing_scholars_count = OngoingScholars.query.count()
    print(ongoing_scholars_count)
    supervisor_count = Supervisors.query.count()
    print(supervisor_count)
    return render_template('dashboard.html', completed_scholars_count=completed_scholars_count, ongoing_scholars_count=ongoing_scholars_count, supervisor_count=supervisor_count)

@app.route('/new_scholar')
def new_scholar():
    return render_template('applicant_add.html')

@app.route('/supervisor')
def supervisor():
    supervisors = Supervisors.query.all()
    return render_template('supervisors.html', supervisors=supervisors)

@app.route('/scholar')
def scholar():
    scholars = OngoingScholars.query.all()
    return render_template('scholar.html', scholars=scholars)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
