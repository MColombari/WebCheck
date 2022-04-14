import pathlib
import sqlite3
from sqlite3 import Error

chatTable = """     CREATE TABLE IF NOT EXISTS chat (
                        id integer PRIMARY KEY
                    ); """

recordTable = """   CREATE TABLE IF NOT EXISTS record (
                        chat_id integer,
                        url text,
                        hash text,
                        PRIMARY KEY (chat_id, url)
                        FOREIGN KEY (chat_id) REFERENCES chat (id)
                    );"""

def main():
    path = '{}/SQLiteDB.db'.format(str(pathlib.Path().resolve()))
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(chatTable)
        c.execute(recordTable)
    except Error as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    main()