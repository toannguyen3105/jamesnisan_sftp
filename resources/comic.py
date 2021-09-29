#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import es
from flask_restful import Resource, reqparse

from utils.datetime_format import get_timestamp
from utils.uuid import generate_uuid

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


# ComicItem to CRUD Comic
class ComicItem(Resource):
    def get(self, item_id: str):
        result = es.get(index='movies', doc_type='asia', id=item_id)

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

        result = es.update(index='movies', doc_type='asia', id=item_id, body=body)

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
        result = es.delete(index='movies', doc_type='asia', id=item_id)

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


class ComicItemCreate(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("name",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("description",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("author",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("url",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("keywords",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("email",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    parser.add_argument("revenue",
                        type=float,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def post(self):
        data = self.parser.parse_args()

        body = {
            'name': data["name"],
            'description': data["description"],
            'author': data["author"],
            'url': data["url"],
            'keywords': data["keywords"],
            'email': data["email"],
            'revenue': data["revenue"],
            'timestamp': get_timestamp()
        }

        result = es.index(index='movies', doc_type='asia', id=generate_uuid(), body=body)

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


# ComicList to show comics list
class ComicList(Resource):
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
                        "fields": ["name", "description", "author", "keywords"]
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

        res = es.search(index="movies", doc_type="asia", body=body)

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
