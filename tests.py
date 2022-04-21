"""from interaction import LDB

def main():
    ldb = LDB()
    ldb2 = LDB()

    print(ldb == ldb2)

    sqlB = 'SELECT COUNT(*) FROM chat WHERE id=?'
    ret = ldb.query(sqlB, ('10',))
    ldb.query('INSERT INTO chat(id) VALUES (?)', (5,))
    for rows in ret:
        print('\nNew Row:')
        for row in rows:
            print(row)

if __name__ == '__main__':
    main()"""

from multiprocessing import Process
import hashlib
from urllib.request import urlopen, Request
from time import sleep


class ThreadFind:
    def __init__(self, url_string):
        self.url_string = url_string
        self.ret = None
        self.process = Process(target=self.run, args=(self,))
        self.process.start()

    def run(self):
        url = Request(self.url_string, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(url).read()
        self.ret = hashlib.sha224(response).hexdigest()


t = ThreadFind('http://google.it')
sleep(10)
print(t.ret)
t.process.terminate()
