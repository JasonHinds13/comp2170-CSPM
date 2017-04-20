from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash
from flask_login import login_user, logout_user, current_user, login_required
import requests
from .forms import *
from .models import *

class DBController:
    
    def __init__(self, objec):
        self.obj = objec
        
    def postToDatabase(self):
        db.session.add_new(self.obj)
        db.session.commit()
        
    def readFromDataabase(self):
        pass

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')
    
@app.route("/createProject", methods=["GET","POST"])
def createproj():
    
    form = ProjectForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            desc = form.description.data
            sig = form.sig.data
            
            proj = Project(name=name, description=desc, sig=sig)
            
    return render_template("createproject.html",form=form)
    
@app.route("/createTask", methods=["GET","POST"])
def createtask():
    
    form = TaskForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.assignee.data
            desc = form.description.data
            
            task = Task(assignee=name, description=desc, progess=0)
            
    return render_template("createtask.html",form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            pass
    return render_template("signup.html",form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
             
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
