# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import current_app, current_user, login_required
from app.models import Permission
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html')

    return render_template('enterprise/index.html')



@main.route('/search')
def search():
    return render_template('enterprise/search.html')


@main.route('/result')
def result():
    return render_template('enterprise/result.html')


@main.route('/user/<username>')
def user(username):
    pass
