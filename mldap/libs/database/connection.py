#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 2016/12/18 15:29
# file: connection.py
from __future__ import print_function
from __future__ import unicode_literals
import logging

"""

"""


def connect_sqlite(**config):
    """
    dbconfig = {
        'database': path
    }
    """
    import sqlite3
    try:
        con = sqlite3.connect(config['database'], isolation_level=None)
        return con
    except sqlite3.Error as e:
        logging.error('[CONNECTION FAIL!] {} {}'.format(type(e), e))


def connect_mysql(**config):
    """
        dbconfig = {
        'host': 'xxx.xxx.xxx.xxx',
        'user': 'username',
        'password': 'password',
        'port': prot_number,
        'database': 'database_name',
        'charset': 'encoding',
        'autocommit':True or False,
        'pool_name': 'polling_name',    # not_required
        'pool_size': pool_size,         # not_required
        'ssl_ca':'ca.pem',              # not_required
        'ssl_cert':'client-cert.pem',   # not_required
        'ssl_key':'client-key.pem',     # not_required
        'ssl_verify_cert':True or False # not required
    }
    """
    import mysql.connector
    try:
        con = mysql.connector.connect(**config)
        return con
    except mysql.connector.Error as e:
        logging.error('[CONNECTION FAIL!] {} {}'.format(type(e), e))


def connect_oracle(**config):
    import cx_Oracle
    try:
        pass
    except cx_Oracle.Error as e:
        logging.error('[CONNECTION FAIL!] {} CODE:{} MESSAGE:{}'.format(
            type(e), e.code, e.message))


# no-sql


class __Connection(object):
    def __init__(self, connection):
        self.connection = connection

    def cursor(self):
        return self.connection()

    def close(self):
        pass


def connect_redis(**config):
    """
    dbconfig = {
        'host':'xxx.xxx.xxx.xxx',
        'port':'port_number',
        'database': 'databasename'
    }
    """
    import redis
    try:
        con = __Connection(lambda: redis.Redis(host=config['host'] or '',
                                               port=config['port'] or 6379, db=config['database']))
        return con
    except redis.ConnectionError as e:
        logging.error('[CONNECTION FAIL!] {} {}'.format(type(e), e))


def connect_mongo(**config):
    """
    dbconfig = {
        'host': 'xxx.xxx.xxx.xxx',
        'user': 'username',
        'password': 'password',
        'port': prot_number,
        'database': databasename
        'ssl_ca':'ca.pem',              # not_required
        'ssl_cert':'client-cert.pem',   # not_required
        'ssl_key':'client-key.pem',     # not_required
        'ssl_verify_cert':True or False # not required
        'authMechanism':None, 'SCRAM-SHA-1','MONGODB-CR'
    }
    """
    import pymongo
    import pymongo.errors

    class __MongodbConnection(__Connection):
        def __init__(self, **config):
            # TODO password urlencode
            uri = 'mongodb://'
            if 'user' in config:  # 'mongodb://user:password/database'
                uri = '%s%s:%s@%s:%s/%s' % (uri, config['user'],
                                            config['password'], config['host'],
                                            config['port'], config['database'])
                if 'authMechanism' in config and config['authMechanism']:
                    # 'mongodb://user:password/database?authMechanism='
                    uri = '%s?authMechanism=%s' % (uri,
                                                   config['authMechanism'])
            else:  # 'mongodb://host:port'
                uri = '%s%s:%s/%s' % (uri, config['host'],
                                      config['port'], config['database'])

            if 'ssl_verify_cert' in config and config['ssl_verify_cert']:
                ssl = 'ssl=true&ssl_ca_certs=%s&ssl_certfile=%s&ssl_keyfile=%s'
                ssl %= (config['ssl_ca'], config['ssl_cert'], config['ssl_key'])

                if '?' in uri:
                    uri = '%s%s' % (uri, ssl)
                else:
                    uri = '%s?%s' % (uri, ssl)
            self.uri = uri

        def cursor(self):
            db = pymongo.MongoClient(self.uri)
            return db

    try:

        con = __MongodbConnection(**config)
        return con
    except pymongo.errors.ConnectionFailure as e:
        logging.error('[CONNECTION FAIL!] {} {}'.format(type(e), e))


if __name__ == '__main__':
    dbconfig = {
        'host': '222.201.145.184',  # 默认127.0.0.1
        'user': 'da',
        'password': '123456',
        'port': 3306,  # 默认是3306
        'database': '123',
        'charset': 'utf8',  # 默认是utf8
        'autocommit': True,
        'pool_name': 'pool1',
        'pool_size': 3,
        'ssl_ca': 'ca.pem',
        'ssl_cert': 'client-cert.pem',
        'ssl_key': 'client-key.pem',
        'ssl_verify_cert': True
    }
    conn = connect_mongo(**dbconfig)
    print(conn.uri)
    # con = connect(**dbconfig)
    # print dir(con)
    # cursor = con.cursor()
    # cursor.execute('select * from test')
    # print cursor.fetchall()
