import sqlite3
import pathlib


class LocalDB:

    @staticmethod
    def query(query, *params):
        try:
            db_conn = sqlite3.connect('{}/SQLiteDB.db'.format(str(pathlib.Path().resolve())))
            ret = list()
            cur = db_conn.cursor()

            if len(params) == 0:
                cur.execute(query)
                ret.append(cur.fetchall())
            else:
                for param in params:
                    cur.execute(query, param)
                    ret.append(cur.fetchall())
            db_conn.commit()
            return ret
        except Exception as e:
            raise e
        finally:
            db_conn.close()


"""    def getData(self, query, param=None):
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
                                                    """
