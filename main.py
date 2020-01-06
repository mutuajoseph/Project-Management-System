from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt
import datetime
import pygal


DB_URL = 'postgresql://postgres:wamzy@127.0.0.1:5432/pmsystem'
DB_URL_PRODUCTION ='postgres://xfdzbmxontsqnb:aa88dca22664f8a7e68124b65e4b98bd481ed2af9e88a09b85677a66d7ac232c@ec2-54-217-221-21.eu-west-1.compute.amazonaws.com:5432/d1esbj9c2tsod4'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models.projects import ProjectsModel
from models.users import UserModel

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login',next=request.url))
    return wrap


@app.route('/register', methods=['GET','POST'])
def register():

     # Fetch all inputs from users
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if UserModel.check_email_exist(email):
            flash('Email already exists','danger')
            return redirect(url_for('register'))
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user = UserModel(username=username, email=email, password=hashed_password)
            user.create_task()
            flash('User Successfully Added', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email exists
        if UserModel.check_email_exist(email):
            # Check if the password is valid
            if UserModel.check_password(email, password):
                session['logged_in'] = True
                session['username'] = UserModel.fetch_by_email(email).username
                session['id'] = UserModel.fetch_by_email(email).id
                return redirect(url_for('home'))
            else:
                flash('Wrong login credentials!   Please Try Again!!','danger')
                return redirect(url_for('login'))
        else:
            flash('Email does not exist', 'danger')
    return render_template('login.html')
   

@app.route('/')
@login_required
def home():
    if session:
        
        username = session['username']
        uid = session['id']
        # print(uid)

        projects = ProjectsModel.fetch_records(uid)
        users = UserModel.fetch_records()

        status = [x.status for x in projects]
        print(status)
        pie_chart = pygal.Pie()
        pie_chart.title = 'Incomplete projects vs Complete projects'
        pie_chart.add('ProjectModel',status.count('Complete'))
        pie_chart.add('ProjectModel',status.count('Incomplete'))
        graph = pie_chart.render_data_uri()

    
        return render_template('index.html', proj=len(projects), user=len(users),graph=graph)
    else:
        flash("Unauthorised Access", "danger")
        return redirect(url_for('login'))

@app.route('/users', methods=['GET','POST'])
def users():
    
    # Fetch all records in users
    users = UserModel.fetch_records()

    return render_template('users.html', users=users)

  

@app.route('/projects', methods=['GET','POST'])
@login_required
def projects():
    if session: 

        username = session['username']
        uid = session['id']
        # Fetch all records in projects
        projects = ProjectsModel.fetch_records(uid)
        # workers = ProjectsModel.
        print(type(projects))
        

        # Fetching all inputs from projects
    
        if request.method == 'POST':
            projectTitle = request.form['projectTitle']
            description = request.form['description']
            cost = request.form['cost']
            timeframe = request.form['timeframe']
            workers = request.form['workers']


            project = ProjectsModel(projectTitle=projectTitle, description=description, cost=cost, timeframe=timeframe,
                                 workers=workers, user_id=uid)

            project.create_task()
            return redirect(url_for('projects'))

        return render_template('projects.html', projects=projects)
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('login'))

# edit a task
@app.route('/project/update/<int:id>', methods=['POST'])
def update_projects(id):
    if request.method == 'POST':
        newProjectTitle = request.form['newProjectTitle']
        newDescription = request.form['newDescription']
        newDateCreated = request.form['newDateCreated']
        newCost = request.form['newCost']
        newTimeframe = request.form['newTimeframe']
        newStatus = request.form['newStatus']
        newWorkers = request.form['newWorkers']

        update_project = ProjectsModel.update_by_id(id=id,newProjectTitle=newProjectTitle,newDescription=newDescription,newDateCreated=newDateCreated,
                                    newCost=newCost,newTimeframe=newTimeframe,newStatus=newStatus, newWorkers=newWorkers)
        
        if update_project:
            print('record successfully updated')
            return redirect(url_for('projects'))
        else:
            print('update unsuccessfull')
            return redirect(url_for('projects'))

@app.route('/user/update/<int:id>', methods=['POST'])
def update_users(id):
    if request.method == 'POST':
        newUsername = request.form['newUsername']
        newEmail = request.form['newEmail']

        update_user = UserModel.update_by_id(id=id, newUsername=newUsername, newEmail=newEmail)

        if update_user:
            print('record successfully updated')
            return redirect(url_for('users'))
        else:
            print('Update unsuccessful')
            return redirect(url_for('users'))
    
# delete a project
@app.route('/project/del/<int:id>', methods=['POST'])
def delete_project(id):
    deleted = ProjectsModel.delete_by_id(id=id)
    if deleted:
        print('successfully deleted')
        return redirect(url_for('projects'))
    else:
        print('record not found')
        return redirect(url_for('projects'))

# delete a user
@app.route('/user/del/<int:id>', methods=['POST'])
def delete_user(id):
    deleted = UserModel.delete_by_id(id=id)
    if deleted:
        print('successfully deleted')
        return redirect(url_for('users'))
    else:
        print('record not found')
        return redirect(url_for('users'))

# Log Out route
@app.route('/logout')
def logoutOperator():
    session.clear()
    flash('You are now logged out','success')

    return redirect(url_for('login'))

if __name__ == "__main__":
    pass