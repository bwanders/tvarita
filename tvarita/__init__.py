#!/usr/bin/env python

from flask import Flask, url_for, render_template, redirect, abort, request
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
    else:
        return ''


def save_page(page, source):
    # fix newlines
    source = source.replace('\r\n','\n')

    # fix pre and post whitespace
    source = source.strip()
    # add newline at end of file
    source = source + '\n'

    # save the actual page
    saved_page = os.path.join(config.page_path, normalize(page))
    with open(saved_page, 'w') as f:
        f.write(source)


def page_exists(page):
    requested_page = os.path.join(config.page_path, normalize(page))
    return os.path.isfile(requested_page)


def render_page(page):
    page_source = get_page_source(page)
    return render_source(page_source)

def render_source(source):
    return markdown.markdown(source, safe_mode='escape', output_format='html5', extensions=['wikilinks'])

@app.route('/')
def index():
    return redirect(url_for('serve_page', page=normalize('start')))


@app.route('/<page>/')
def serve_page(page):
    if normalize(page) != page:
        return redirect(url_for('serve_page', page=normalize(page)))

    if not page_exists(page):
        abort(404)

    result = render_page(page)
    return render_template('page.html', content = result, title = page, page=page)

@app.route('/<page>/edit/')
def edit_page(page):
    if normalize(page) != page:
        return redirect(url_for('edit_page',page=normalize(page)))

    page_source = get_page_source(page)

    return render_template('edit.html', content=page_source, title = page + ' [edit]', page=page)

@app.route('/<page>/edit/', methods=['POST'])
def edit_page_posted(page):
    if normalize(page) != page:
        abort(405)

    new_page_source = request.form['page']

    if request.form['do'] == 'Preview':
        return render_template('edit.html', content=new_page_source, title = page + ' [edit]', page=page, preview=render_source(new_page_source))
    else:
        save_page(page, new_page_source)
        return redirect(url_for('serve_page', page=page))


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(error):
    return render_template('error.html', error=error), error.code

