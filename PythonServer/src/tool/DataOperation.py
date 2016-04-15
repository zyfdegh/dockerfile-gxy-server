# coding=utf-8
import MySQLdb


class DataOperation:
    def __init__(self, host='115.159.157.48', user='secondhand', passwd='zhushijie219211l', db='secondhand', port=3306):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db
        self._port = port

    def connect(self):
        try:
            self._conn = MySQLdb.connect(host=self._host, user=self._user, passwd=self._passwd, db=self._db,
                                         port=self._port, use_unicode=True, charset="utf8")
            return (True, None)
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return (False, e.args[1])

    def query(self, sql):
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql)
            return self._cur
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            print sql
            return None

    def close(self):
        try:
            self._cur.close()
            self._conn.close()
            return (True, None)
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return (False, e.args[1])

    def operate(self, sql):
        try:
            self._cur = self._conn.cursor()
            self._cur.execute(sql)
            self._conn.commit()
            return (True, None)
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            print sql
            return (False, e.args[1])

    def multiOperate(self, sqlList):
        try:
            self._cur = self._conn.cursor()
            for sql in sqlList:
                self._cur.execute(sql)
            self._conn.commit()
            return (True, None)
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            print sqlList
            return (False, e.args[1])


if __name__ == '__main__':
    d = DataOperation()
    d.connect()
    cur = d.query("select * from requirement")
    for c in cur.fetchall():
        print(c)
