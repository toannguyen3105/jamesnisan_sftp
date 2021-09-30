#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db
from resources.item import DownloadItem

__author__ = "@toannguyen3105"

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(DownloadItem, '/download-files')

# 1. Create a flask app
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
