#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 16-12-7 下午1:10
# file: test.py.py


import sqlite3

connection = sqlite3.connect(':memory:')
print sqlite3.apilevel
print sqlite3.threadsafety