#
# TextPrint
# Laboratoire IDHN
#

#
# Importations
#
from flask import render_template
from flask import request, make_response, redirect, session, escape
from app import app
from db import db_add, db_init, db_search
from flask import jsonify
import json
import os.path
import calendar
import time
from langdetect import detect
import chardet    
import io

#
# Route de base
# 
@app.route('/')
def index():
    db_init()
    if 'connect' in session:
        if session['connect'] == 1:
            return redirect('/page')
    return render_template('index.html')

@app.route('/page')
def page():
    if 'connect' in session:
        if session['connect'] == 1:
            return render_template('page.html')
    return redirect('/')

@app.route('/deconnexion')
def deconnexion():
    session['connect'] = 0
    return redirect('/')

@app.route('/connexion')
def connexion():
    session['connect'] = 1
    return redirect('/page')