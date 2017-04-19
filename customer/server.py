#!/usr/bin/env python
import json
import logging
import tornado
import tornado.web
import tornado.escape
import pymongo
import psycopg2
import sys
import uuid

from getpass import getuser
from contextlib import contextmanager

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_hdl = logging.StreamHandler(sys.stdout)
log_hdl.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'))
log_hdl.setLevel(logging.DEBUG)
log.addHandler(log_hdl)

class localBackend:
    def __init__(self):
        self.dbuser = getuser()
        self.dbhost = 'localhost'
        self.dbpwd = 'unsafe'
        self.tblname = 'customer'
        try:
            self.dbsess = psycopg2.connect(dbname='postgres',
                                      user=self.dbuser,
                                      host=self.dbhost,
                                      password=self.dbpwd)
        except psycopg2.Error as e:
            log.error(e)
        self.mgclient = pymongo.MongoClient('localhost:27017')

    @contextmanager
    def cur_hdl(self):
        ''' manage pg cursor '''
        cur = self.dbsess.cursor()
        try:
            yield cur
        finally:
            cur.close()
            self.dbsess.commit()

    def init_pg(self):
        ''' create customer table if dne '''
        with self.cur_hdl() as cur:
            cmd = """ CREATE TABLE customers (
                        c_uid UUID PRIMARY KEY NOT NULL,
                        c_name VARCHAR(255) NOT NULL,
                        c_income INTEGER,
                        c_addr VARCHAR(255),
                        c_date DATE NOT NULL DEFAULT CURRENT_DATE
                    )
                """
            try:
                cur.execute(cmd)
            except psycopg2.Error as e:
                log.info(e)

    def insert_pg(self, username, income=None, address=None, dt_create=None):
        ''' insert customer info into customers table '''
        unique_id = str(uuid.uuid4())
        with self.cur_hdl() as cur:
            try:
                cur.execute("INSERT INTO customers (c_uid, c_name, c_income, c_addr) VALUES (%s, %s, %s, %s)",
                            (unique_id, username, income, address))
            except psycopg2.Error as e:
                log.error(e)
        res = self.insert_mg(self.get_by_uid_pg(unique_id))
        log.info(res)
        return unique_id

    def get_by_uid_pg(self, c_uid=None):
        ''' get customer info by uuid '''
        with self.cur_hdl() as cur:
            res = {}
            try:
                cur.execute("SELECT * FROM customers")
                for rec in cur:
                    if c_uid is not None:
                        if rec[0] == c_uid:
                            res = {'uuid':rec[0],
                                   'username':rec[1],
                                   'income':rec[2],
                                   'address':rec[3],
                                   'created': str(rec[4])}
                            break
                    else:
                        log.info(rec)
                        res[rec[0]] = rec[1]
                return False if not res else res
            except psycopg2.Error as e:
                log.error(e)

    def init_mg(self):
        self.mgclient.dbc.add_user(self.dbuser, self.dbuser, roles=[{'role':'readWrite','db':'dbc'}])

    def insert_mg(self, customer=None):

        if customer:
            customers = self.mgclient.dbc.customers
            log.info(customers)
            res = customers.insert(customer)
            log.info(res)

class CustomerHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            uid = self.get_argument('uuid', None)
        except AssertionError as e:
            print str(e)
        log.info(uid)
        lb = localBackend()
        res = lb.get_by_uid_pg(uid)
        if not res:
            self.set_status(404)
        else:
            log.info(res)
            self.write(res)

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        lb = localBackend()
        log.info(data)
        username = data['username'] if data['username'] else None
        income = data['income'] if data['income'] else ''
        address = data['address'] if data['address'] else ''
        uid = lb.insert_pg(username, income, address)
        if uid:
            data['uuid'] = uid
            self.write(data)
        else:
            self.clear()
            self.set_status(500)

def customer_app():
    return tornado.web.Application([
        (r"/customer", CustomerHandler),
    ])

def main():

    lb = localBackend()
    lb.init_pg()
    lb.init_mg()
    app = customer_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
