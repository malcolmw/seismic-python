import os
import seispy
import sqlite3

class Database(object):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS event
                         (originid INT, eventid INT PRIMARY, author TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS origin
                         (latitude REAL, longitude REAL, depth REAL,
                         time REAL, originid INT PRIMARY, eventid INT,
                         narrivals INT, author TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS station
                         (stacode TEXT PRIMARY, latitude REAL, longitude REAL,
                         elevation REAL, time REAL, endtime REAL, netcode TEXT,
                         arraycode TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS wfdisc
                         (stacode TEXT PRIMARY, channel TEXT PRIMARY,
                         time REAL PRIMARY, endtime REAL PRIMARY,
                         dir TEXT, file TEXT, datatype TEXT, nsamples INT,
                         samplerate REAL, author TEXT)
                         """)

    def read_antelope(self, path):
        if os.path.isfile("%s.event" % path):
            inf = open("%s.event" % path)
            for line in inf:
                data = line.split()
                data = [int(data[0]), int(data[2]), data[3]]
                self.cur.execute("""
                                 INSERT INTO event
                                 (eventid, originid, author)
                                 VALUES ({}, {}, '{}')
                                 """.format(*data))
            inf.close()
        if os.path.isfile("%s.origin" % path):
            inf = open("%s.origin" % path)
            for line in inf:
                data = line.split()
                data = [float(v) for d in data[:4] +\
                       [int(v) for d in data[4:6]] +\
                       [int(data[7])] +\
                       [data[23]]
                self.cur.execute("""
                                 INSERT INTO origin
                                 (latitude, longitude, depth, time, originid,
                                  eventid, narrivals, author)
                                 VALUES ({}, {}, {}, {}, {}, {}, {}, '{}')
                                 """.format(*data))
            inf.close()
