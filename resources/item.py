#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP
from flask_restful import Resource, reqparse

from models.item import ItemModel

from utils.datetime_format import get_timestamp, get_date_time_from_timestamp

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']

FTP_HOST = 'ftp.dlptest.com'
FTP_USER = 'dlpuser'

# Get new password: https://dlptest.com/ftp-test/
FTP_PASS = 'rNrKYTX9g7z3RgJRmxWuGHbeu'
FTP_PORT = 21


# DownloadItem download file
class DownloadItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("file_name",
                        type=str,
                        required=False,
                        help="This field cannot be blank.",
                        )

    def get(self):
        data = self.parser.parse_args()

        file_name = data["file_name"] if data["file_name"] else "README"

        # LOGIN FTP
        host = FTP_HOST
        username = FTP_USER
        passwd = FTP_PASS
        port = FTP_PORT

        print(f'host:{host}, username:{username} passwd:{passwd}, port: {port}')

        # instance of ftp
        ftp = FTP()

        # set the debig level
        ftp.set_debuglevel(2)

        # connect to ftp
        ftp.connect(host=str(host), port=int(port))
        print('connected')

        # login
        print('login in.....')
        if username:
            if passwd:
                ftp.login(user=username, passwd=passwd)
            else:
                print('Password required')
                exit(0)
        else:
            # login without username and password
            ftp.login()
        # return the dirs list and ftp object

        ftp.cwd('20210930')
        ftp.retrlines('LIST')

        # 5.Upload the file to the server via ftp.
        with open(file_name, "rb") as file:
            ftp.retrlines('LIST')

            # use FTP's STOR command to upload the file
            ftp.storbinary(f"STOR {file_name}", file)

        # 2. Download a file from the server
        with open(file_name, 'wb') as fp:
            result = ftp.retrbinary(f"RETR {file_name}", fp.write)

        # 3. Covert the file to bytecode
        with open(file_name, 'rb') as f:
            contents = f.read()

            print(contents)

            #  4. File content should be saved to sqlite db
            item = ItemModel(contents, get_timestamp(), "Tony", None, None)
            item.save_to_db()

        # FTP QUIT
        ftp.quit()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": {
                       "file_name": file_name,
                       "message": result if result else None
                   },
                   "pagination": {
                       "total": None
                   },
                   "time": get_timestamp(),
                   "time_str": get_date_time_from_timestamp()
               }, 200
