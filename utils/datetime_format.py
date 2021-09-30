#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

date_format = ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
date_time_format = date_format[0]
date_time_format_momo = date_format[1]


def get_timestamp():
    now = datetime.now()
    return int(datetime.timestamp(now))


def get_date_time_from_timestamp():
    now = datetime.now()
    return datetime.fromtimestamp(int(datetime.timestamp(now))).strftime(date_time_format)
