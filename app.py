from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt
import datetime


DB_URL = 'postgresql://postgres:wamzy@127.0.0.1:5432/pmsystem'

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
                return redirect(url_for('home'))
            else:
                flash('Wrong login credentials','danger')
                return redirect(url_for('login'))
        else:
            print('Email does not exist', 'danger')

    return render_template('login.html')
   

@app.route('/')
@login_required
def home():

    projects = ProjectsModel.fetch_records()

    
    
    return render_template('index.html', proj=len(projects))

@app.route('/users', methods=['GET','POST'])
def users():
     
    # Fetch all records in users
    users = UserModel.fetch_records()

    # Fetch all inputs from users
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if UserModel.check_email_exist(email):
            flash('Email exist','danger')
            return redirect(request.url)
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user = UserModel(username=username, email=email, password=hashed_password)
            user.create_task()
        flash('User Successfully Added')
        return redirect(url_for('users'))

    return render_template('users.html', users=users)
  

@app.route('/projects', methods=['GET','POST'])
@login_required
def projects():

    # Fetch all records in projects
    projects = ProjectsModel.fetch_records()
    # workers = ProjectsModel.
    print(type(projects))
    

    # Fetching all inputs from projects
   
    if request.method == 'POST':
        projectTitle = request.form['projectTitle']
        description = request.form['description']
        dateCreated = request.form['dateCreated']
        cost = request.form['cost']
        timeframe = request.form['timeframe']
        status = request.form['status']
        workers = request.form['workers']


        project = ProjectsModel(projectTitle=projectTitle, description=description, dateCreated=dateCreated, cost=cost, timeframe=timeframe,
                            status=status, workers=workers)

        project.create_task()
        return redirect(url_for('projects'))

    return render_template('projects.html', projects=projects)

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