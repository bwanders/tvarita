#!/usr/bin/env python

from flask import Flask, url_for, render_template, redirect, abort
import os
import markdown

import config

app = Flask(__name__)


def normalize(page):
    return page.replace('.', '')


def get_page_source(page):
    if page_exists(page):
        requested_page = os.path.join(config.page_path, normalize(page))
        with open(requested_page) as f:
            return f.read()


def page_exists(page):
    requested_page = os.path.join(config.page_path, normalize(page))
    return os.path.isfile(requested_page)


@app.route('/')
def index():
    return redirect(url_for('serve_page', page=normalize('start')))


@app.route('/<page>')
def serve_page(page):
    if normalize(page) != page:
        return redirect(url_for('serve_page', page=normalize(page)))

    if not page_exists(page):
        abort(404)

    page_source = get_page_source(page)
    result = markdown.markdown(page_source, safe_mode='escape', output_format='html5')
    return render_template('page.html', content = result, title = page)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

