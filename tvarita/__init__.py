#!/usr/bin/env python

from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Index"

@app.errorhandler(404)
def page_not_found(error):
    print error
    return render_template('page_not_found.html'), 404

