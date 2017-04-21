from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash
from flask_login import login_user, logout_user, current_user, login_required
import requests
from .forms import *
from .models import *

class DBController:
        
    def postToDatabase(self, obj):
        db.session.add_new(obj)
        db.session.commit()
        
    def readFromDataabase(self, obj, stat):
        if stat == 'first':
            return obj.first()
        elif stat == 'all':
            return obj.query.all()
    
dbcontroller = DBController()

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
@app.route("/createProject", methods=["GET","POST"])
def createproj():
    
    form = ProjectForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            desc = form.description.data
            sig = form.sig.data
            
            proj = Project(name=name, description=desc, sig=sig)
            
            dbcontroller.postToDatabase(proj)
            
    return render_template("createproject.html",form=form)
    
@app.route("/createTask", methods=["GET","POST"])
def createtask():
    
    form = TaskForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.assignee.data
            desc = form.description.data
            project = form.projectname.data
            
            pObj = Project.query.filter_by(name=project)
            proj = dbcontroller.readFromDataabase(pObj, 'first')
            
            task = Task(pid=proj.pid, assignee=name, description=desc, progess=0)
            
            dbcontroller.postToDatabase(task)
            
    return render_template("createtask.html",form=form)

@app.route("/viewProjects", methods=["GET"])
def viewproj():
    projects = dbcontroller.readFromDataabase(Project(), 'all')
    return render_template("viewprojects.html", projects=projects)

@app.route("/viewTasks", methods=["GET"])
def viewtasks():
    tasks = dbcontroller.readFromDataabase(Task(), 'all')
    return render_template("viewtasks.html",tasks=tasks)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data
            sig = form.special_interest_group.data
            acctype = form.acctype.data
            
            user = SystemUser(first_name=first_name, last_name=last_name, username=username,
            password=password, sig=sig, acctype=acctype)
            
            dbcontroller.postToDatabase(user)
            
    return render_template("signup.html",form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            userObj = SystemUser.query.filter_by(username=username, password=password)
            user = dbcontroller.readFromDataabase(userObj, 'first')
            #user = SystemUser(acctype='admin') ###Just for testing purposes
            
            if user is not None:
                session['logged_in'] = True
                session['account_type'] = user.acctype ## store account type to handle MVC stuff
                flash('You were logged in')
                return redirect(url_for('home'))
                
    return render_template('login.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
    
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
