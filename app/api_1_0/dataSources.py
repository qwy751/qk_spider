# -*- coding: utf-8 -*-
import json
from datetime import time, datetime

import pickle
from flask import redirect, request, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from app.api_1_0.errors import bad_request
from app.api_1_0.models import InnerResult
from app.datasource import ds
from flask_login import current_user, login_user, login_required
from app.datasource.query import Query
from flask_restful import reqparse, Resource
from app import api as api_restful, db
from ..datasource.query import Query
from . import api


@api.route('/test')
def test():
    print("here")
    return "ok"


class DataSources(Resource):
    """
    Restful for query
    """
    # decorators = []
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided', location='json')
        super(DataSources, self).__init__()

    def get(self):
        args = request.args.to_dict()
        have_result = InnerResult.query.filter_by(condition=str(args)).first()
        # if have_result is not None and have_result is not None:
        #     r = pickle.loads(have_result.result)
        #     return r

        # TODO:
        return
        query = Query()
        result = query.query(**args)

        inner_result = InnerResult(condition=str(args), result=pickle.dumps(result), received_time=datetime.now())
        db.session.add(inner_result)
        db.session.commit()
        return result

api_restful.add_resource(DataSources, '/data', endpoint='data')

