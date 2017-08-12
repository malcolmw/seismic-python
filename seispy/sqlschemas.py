import os
import seispy
import sqlite3

class SeismicDB(object):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS arrival
                         (arrivalid INT, stacode TEXT, channel TEXT, time REAL,
                         phase TEXT, author TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS assoc
                         (arrivalid INT, originid INT, residual REAL)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS detection
                         (stacode TEXT, channel TEXT, time REAL, label TEXT,
                         snr REAL)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS event
                         (originid INT, eventid INT, author TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS origin
                         (latitude REAL, longitude REAL, depth REAL,
                         time REAL, originid INT, eventid INT,
                         narrivals INT, author TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS station
                         (stacode TEXT, latitude REAL, longitude REAL,
                         elevation REAL, time REAL, endtime REAL, netcode TEXT,
                         arraycode TEXT)
                         """)
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS wfdisc
                         (stacode TEXT, channel TEXT, time REAL, endtime REAL,
                         dir TEXT, file TEXT, datatype TEXT, nsamples INT,
                         samplerate REAL, author TEXT)
                         """)

    def convert_antelope(self, path):
        if os.path.isfile("%s.arrival" % path):
            inf = open("%s.arrival" % path)
            for line in inf:
                data = line.split()
                data = [int(data[2]), data[0], data[6], float(data[1]), data[7],
                        data[23]]
                print("arrival: ({}, '{}', '{}', {}, '{}', '{}')".format(*data))
                self.cur.execute("""
                                 INSERT INTO arrival
                                 (arrivalid, stacode, channel, time, phase,
                                 author)
                                 VALUES ({}, '{}', '{}', {}, '{}', '{}');
                                 """.format(*data))
            inf.close()
        if os.path.isfile("%s.assoc" % path):
            inf = open("%s.assoc" % path)
            for line in inf:
                data = line.split()
                data = [int(data[0]), int(data[1])]
                print("assoc: ({}, {})".format(*data))
                self.cur.execute("""
                                 INSERT INTO assoc
                                 (arrivalid, originid)
                                 VALUES ({}, {});
                                 """.format(*data))
            inf.close()
        if os.path.isfile("%s.detection" % path):
            inf = open("%s.detection" % path)
            for line in inf:
                data = line.split()
                data = [data[2],
                        data[3],
                        float(data[4]),
                        data[6],
                        float(data[-1])]
                print("detection: ('{}', '{}', {}, '{}', {})".format(*data))
                self.cur.execute("""
                                 INSERT INTO detection
                                 (stacode, channel, time, label, snr)
                                 VALUES ('{}', '{}', {}, '{}', {});
                                 """.format(*data))
            inf.close()
        if os.path.isfile("%s.event" % path):
            inf = open("%s.event" % path)
            for line in inf:
                data = line.split()
                data = [int(data[0]), int(data[2]), data[3]]
                print("event ({}, {}, '{}')".format(*data))
                self.cur.execute("""
                                 INSERT INTO event
                                 (eventid, originid, author)
                                 VALUES ({}, {}, '{}');
                                 """.format(*data))
            inf.close()
        if os.path.isfile("%s.origin" % path):
            inf = open("%s.origin" % path)
            for line in inf:
                data = line.split()
                data = [float(v) for v in data[:4]] +\
                       [int(v) for v in data[4:6]] +\
                       [int(data[7])] +\
                       [data[23]]
                print("origin ({}, {}, {}, {}, {}, {}, {}, '{}')".format(*data))
                self.cur.execute("""
                                 INSERT INTO origin
                                 (latitude, longitude, depth, time, originid,
                                  eventid, narrivals, author)
                                 VALUES ({}, {}, {}, {}, {}, {}, {}, '{}');
                                 """.format(*data))
            inf.close()
