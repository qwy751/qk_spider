# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import current_app, current_user, login_required
from app.models import Permission
from . import enterprise


@enterprise.route('/', methods=['GET', 'POST'])
def index():
    return render_template('enterprise/index.html')


@enterprise.route('/search')
def search():
    return render_template('enterprise/search.html')


@enterprise.route('/result')
def result():
    return render_template('enterprise/result.html')


@enterprise.route('/user/<username>')
def user(username):
    pass
