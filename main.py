#--------------------------------------------------------
"""
Description: This file contains the configuration and Routing
@author: Debashis Rout
"""
#--------------------------------------------------------

import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__, template_folder='templates', static_url_path='/uploads')
app.secret_key = b'_5#y2LF4Q8zec]/'

# File Upload folder
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
#app.config['UPLOAD_PATH'] = join(dirname(realpath(__file__)), 'uploads/')
#print(app.config['UPLOAD_PATH'])

# DB Settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dezzex'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    This is signup for User
    :return:
    """
    success_msg = ''
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        hash_password = hashlib.md5(password.encode())
        #print(hash_password.hexdigest())

        # MySQL Connection
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM MyUsers WHERE email = %s AND status = %s ", (username, '1'))
            data = cur.fetchone()
            cur.close()
        except Exception as e:
            #print(str(e))
            #return (str(e))
            success_msg = str(e)

        # storing into session and redirect to profile page
        #print(data)
        if data[3] == hash_password.hexdigest():
            session['email'] = data[2]
            return redirect(url_for('my_profile'))

    return render_template('login.html', msg=success_msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This is signup for User
    :return:
    """
    success_msg = ''
    if request.method == "POST":
        details = request.form
        name = details['name']
        email = details['email']
        password = details['password']
        hash_password = hashlib.md5(password.encode())
        #print(hash_password.hexdigest())
        phone = details['phone']
        passport = details['passport']

        # MySQL connection
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO MyUsers(name, email, password, phone, passport, status) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, hash_password.hexdigest(), phone, passport, '1'))
            mysql.connection.commit()
            cur.close()

            # Redirect to sign up page with success message
            success_msg = 'Successfully registered. Email sent.'

        except Exception as e:
            #print(str(e))
            #return (str(e))
            success_msg = str(e)

    return render_template('signup.html', msg=success_msg)


@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    """
    This is my_profile for User
    :return:
    """
    #email = 'deba123@email.com'
    #if 'email' in session:
    #    return 'Logged in as %s' % session['email']

    email = session['email']
    #print(email)
    # MySQL Connection
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MyUsers WHERE email = %s ", (email, ))
    profile_data = cur.fetchone()

    success_msg = ''
    if request.method == "POST":
        if 'file' not in request.files:
            success_msg = 'No file attached!'
        else:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                #uploaded_file.save(app.config['UPLOAD_PATH'] + filename)
                uploaded_file.save('uploads/' + filename)

                # Update file name into MyUsers table
                cur.execute("UPDATE MyUsers SET profile_photo = %s WHERE email = %s", (filename, email))
                mysql.connection.commit()

        return redirect(url_for('my_profile'))

    cur.close()
    return render_template('my_profile.html', data=profile_data)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    This is logout for User
    :return:
    """
    #email = session['email']
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()