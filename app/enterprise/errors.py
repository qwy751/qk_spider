# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify


from . import enterprise


@enterprise.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('enterprise/403.html'), 403


@enterprise.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('enterprise/404.html'), 404


@enterprise.app_errorhandler(500)
def internal_server_error(e):
    return render_template('enterprise/500.html'), 500
