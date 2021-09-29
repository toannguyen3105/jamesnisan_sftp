#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import es
from flask_restful import Resource, reqparse

from utils.datetime_format import get_timestamp
from utils.uuid import generate_uuid

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']

INDEX = 'ssadocs'
DOC_TYPE = 'document'


# SsadocItem to CRUD Ssadoc
class SsadocItem(Resource):
    def get(self, item_id: str):
        result = es.get(index=INDEX, doc_type=DOC_TYPE, id=item_id)

        if result:
            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": result,
                       "pagination": {
                           "total": len(result)
                       },
                       "time": get_timestamp()
                   }, 200

    def put(self, item_id: str):
        body = {
            "doc": {
                'updated_at': get_timestamp()
            }
        }

        result = es.update(index=INDEX, doc_type=DOC_TYPE, id=item_id, body=body)

        if result:
            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": result,
                       "pagination": {
                           "total": len(result)
                       },
                       "time": get_timestamp()
                   }, 200

    def delete(self, item_id: str):
        result = es.delete(index=INDEX, doc_type=DOC_TYPE, id=item_id)

        if result:
            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": result,
                       "pagination": {
                           "total": len(result)
                       },
                       "time": get_timestamp()
                   }, 200


# SsadocItemCreate to create new item
class SsadocItemCreate(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("table_name",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("table_summary",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("table_description",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("url",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def post(self):
        data = self.parser.parse_args()

        body = {
            'table_name': data["table_name"],
            'Table Summary': data["table_summary"],
            'Table Description': data["table_description"],
            'url': data["url"],
            'timestamp': get_timestamp()
        }

        result = es.index(index=INDEX, doc_type=DOC_TYPE, id=generate_uuid(), body=body)

        if result:
            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": result,
                       "pagination": {
                           "total": len(result)
                       },
                       "time": get_timestamp()
                   }, 200


# SsadocList to show ssa list
class SsadocList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        type=str,
                        required=False,
                        help="This field cannot be blank.",
                        location='args'
                        )

    def get(self):
        data = self.parser.parse_args()
        keyword = data["name"]

        if keyword:
            body = {
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["table_name", "Table Summary", "Table Description"]
                    }
                }
            }

        else:
            body = {
                "size": 100,
                "query": {
                    "match_all": {
                    }
                }
            }

        res = es.search(index=INDEX, doc_type=DOC_TYPE, body=body)

        if res:
            items = res['hits']['hits']

            return {
                       "error": None,
                       "status": STATUS_CODES[0],
                       "result": [item for item in items],
                       "pagination": {
                           "total": len(items)
                       },
                       "time": get_timestamp()
                   }, 200
