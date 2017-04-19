#!/usr/bin/python

import os
from delBibsApi import analytics_xml
from flask import Flask, flash, redirect, render_template, request, session, url_for
app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
URL=str('https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports')
PATH=str('/shared/Emory University Libraries/Reports/ACOOPE5/Deleted_bibs')
APIKEY=str('l7xx00334afab90e47c9aa950cdc92b405b9')
LIMIT=str('1000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html', name=app.config['USERNAME'])

@app.route('/requesting', methods=['GET', 'POST'])
def requesting():
    xml=analytics_xml(URL,APIKEY,PATH,LIMIT)
    return render_template('request.html', xml=xml)

@app.route('/good_bye', methods=['GET', 'POST'])
def good_bye():
    return render_template('good_bye.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('good_bye'))
