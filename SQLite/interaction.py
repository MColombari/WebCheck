import sqlite3


class LDB:
    def __init__(self, dbName):
        self.dbName = dbName
        self.dbConn = sqlite3.connect(self.dbName)

    def getData(self, query, param=None):
        cur = self.dbConn.cursor()
        if param != None:
            cur.execute(query, param)
        else:
            cur.execute(query)
        return cur.fetchall()

    def insertData(self, query, param):
        cur = self.dbConn.cursor()
        cur.execute(query, param)
        self.dbConn.commit()

    def genericQuery(self, query, *params):
        ret = list()
        cur = self.dbConn.cursor()

        if len(params) == 0:
            cur.execute(query)
            ret.append(cur.fetchall())
        else:
            for param in params:
                cur.execute(query, param)
                ret.append(cur.fetchall())
        self.dbConn.commit()
        return ret


    def __del__(self):
        self.dbConn.close()