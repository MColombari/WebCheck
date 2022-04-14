from interaction import LDB

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
    main()