#!/usr/bin/env python
from getpass import getuser
import tornado
import tornado.web
import tornado.escape
import pymongo
import psycopg2
import uuid

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
            print str(e)

    def init_pg(self):
        cur = self.dbsess.cursor()
        try:
            cmd = """ CREATE TABLE customers (
                        c_uid UUID PRIMARY KEY NOT NULL,
                        c_name VARCHAR(255) NOT NULL,
                        c_income INTEGER,
                        c_addr VARCHAR(255),
                        c_date DATE NOT NULL DEFAULT CURRENT_DATE
                    )
                """
            cur.execute(cmd)
            cur.close()
            self.dbsess.commit()
        except psycopg2.Error as e:
            print str(e)

    def insert_pg(self, username, income=None, address=None, dt_create=None):
        cur = self.dbsess.cursor()
        try:
            cur.execute("INSERT INTO customers (c_uid, c_name, c_income, c_addr) VALUES (%s, %s, %s, %s)",
                        (str(uuid.uuid4()), username, income, address))
            cur.close()
            self.dbsess.commit()
            return True
        except psycopg2.Error as e:
            print str(e)

    def get_by_uid_pg(self, c_uid):
        cur = self.dbsess.cursor()
        try:
            cur.execute("SELECT * FROM customers")
            res = None
            for rec in cur:
                if rec[0] == c_uid:
                    res = {'uuid':rec[0],
                           'username':rec[1],
                           'income':rec[2],
                           'address':rec[3],
                           'created': str(rec[4])}
                    break
            cur.close()
            self.dbsess.commit()
            return False if not res else res
        except psycopg2.Error as e:
            print str(e)

class CustomerHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            uid = self.get_argument('uuid', True)
        except AssertionError as e:
            print str(e)
        print uid
        lb = localBackend()
        if uid:
            res = lb.get_by_uid_pg(uid)
            if not res:
                self.set_status(404)
            else:
                print res
                self.write(res)
        #lb.insert()

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        print data
        lb = localBackend()
        username = data['username'] if data['username'] else None
        income = data['income'] if data['income'] else ''
        address = data['address'] if data['address'] else ''
        if lb.insert_pg(username, income, address):
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
    app = customer_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
