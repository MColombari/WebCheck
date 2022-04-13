from interaction import LDB

def main():
    ldb = LDB(r"/Users/mattiacolombari/Desktop/Utils/Python/SQLite/pythonsqlite.db")

    sqlA = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''
    task_1 = ('Analyze the requirements of the app NEW', 1, 1, 20, '2015-01-01', '2015-01-02')
    task_2 = ('Analyze the requirements of the app NEW 2', 1, 1, 30, '2015-01-01', '2015-01-02')
    task_3 = ('Analyze the requirements of the app NEW 3', 1, 1, 40, '2015-01-01', '2015-01-02')

    sqlB = 'SELECT * FROM tasks WHERE project_id=?'
    ret = ldb.genericQuery(sqlB, (20,), (30,), (40,))
    for rows in ret:
        print('\nNew Row:')
        for row in rows:
            print(row)

if __name__ == '__main__':
    main()