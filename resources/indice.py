#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import es
from flask_restful import Resource, reqparse
from utils.datetime_format import get_timestamp

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


# IndiceItem to delete index
class IndiceItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("index",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def post(self):
        data = self.parser.parse_args()
        index = data["index"]

        res = es.indices.delete(index=index, ignore=[400, 404])

        if res:
            items = sorted(res)

            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": [item for item in items],
                       "pagination": {
                           "total": len(items)
                       },
                       "time": get_timestamp()
                   }, 200


# IndiceList to list index
class IndiceList(Resource):
    def get(self):
        res = es.indices.get_alias("*").keys()

        if res:
            items = sorted(res)

            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": [item for item in items],
                       "pagination": {
                           "total": len(items)
                       },
                       "time": get_timestamp()
                   }, 200
