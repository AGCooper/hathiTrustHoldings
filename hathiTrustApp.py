#!/usr/bin/python

import os
from delBibsApi import analytics_xml
from hathi_config import deleted_config
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html', name=app.config['USERNAME'])

@app.route('/return_files/')
def return_files():
    return send_file('/tmp/id_list.tsv', attachment_filename='hathi_deleted_report.tsv')

@app.route('/requesting', methods=['GET', 'POST'])
def requesting():
    URL=deleted_config("url")
    PATH=deleted_config("path")
    APIKEY=deleted_config("apikey")
    LIMIT=deleted_config("limit")
    tsv = analytics_xml(URL,APIKEY,PATH,LIMIT)
    return render_template('request.html', tsv=tsv)

@app.route('/good_bye', methods=['GET', 'POST'])
def good_bye():
    return render_template('good_bye.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        elif request.form['email'].find('@') == -1:
            error = 'Invalid email' 
        else:
            email = request.form['email']
            session['logged_in'] = True
            flash('You have been logged in ' + email)
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('good_bye'))
