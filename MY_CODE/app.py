from flask import Flask, render_template, url_for, request, session, redirect,flash, message_flashed,Response
from flask_pymongo import PyMongo
import os
from camera import VideoCamera
from threading import Thread
import cv2

global index_add_counter
app= Flask(__name__)

# Here i am writing all code to connect my application with mongoDb and user authentications.
app.config['MONGO_HOST'] ='localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME']="myfyp"

app.config['SECRET_KEY'] = "You_r_secret"
mongo =  PyMongo(app,config_prefix ="MONGO")
# app.secret_key == "keep it secret"
@app.route('/')
def home():
  # if 'username' in session:
  #       return 'You are logged in as ' + session['username']
  return  render_template('page_home3.html')

@app.route('/about')
def about():
    return render_template('page_about3.html')

@app.route('/contact')
def contact():
    return render_template('page_contact.html')


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one ({'name': request.form['username']})
        if login_user:
            if  (request.form['pass'] == login_user['password']):
                # if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                    session['username'] = request.form['username']
                    return redirect(url_for('profile_main'))
            # return 'Invalid username/password combination'
        if (not login_user) or ((request.form['pass'] != login_user['password'])):
            flash("Invalid Username/Password")
    return render_template('page_login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})
        if existing_user is None:
            # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            password = request.form['pass']
            users.insert({'name': request.form['username'], 'password': password})
            session['username'] = request.form['username']
            return redirect(url_for('profile_main'))
        # return 'That username already exists!'
    return render_template('page_registration.html')

@app.route('/profile')
def profile_main():
    user = session["username"]
    return render_template('page_profile.html',user=user)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


        # frame = Thread(target=camera.get_frame())
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/my_projects')
def my_projects():
    user = session["username"]
    return render_template('page_profile_projects.html',user=user)
@app.route('/my_history')
def my_history():
    user = session["username"]
    return render_template('page_profile_history.html',user =user)
@app.route('/my_profile')
def my_profile():
    user = session["username"]
    return render_template('page_profile_me.html',user = user)

@app.route('/User_Guide')
def User_Guide():
    user = session["username"]
    return render_template('User_guide.html',user = user)

@app.route('/New_Project')
def New_Project():
    user = session["username"]
    return render_template('New_Project.html',user = user)

#
# @app.route('/release_vidoe')
# def release_vidoe():
#     user = session["username"]
#
#     VideoCamera.destroy()
#     return render_template('page_profile.html',user=user)


if __name__ ==('__main__'):
    # app.secret_key == os.urandom(50)
    app.run(debug=True)
