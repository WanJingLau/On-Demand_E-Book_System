import pyodbc as db

conn = db.connect(Driver="{ODBC Driver 17 for SQL Server}", Server="tcp:ebook4006.database.windows.net,1433", Database="ebookDB", Uid="ebook", Pwd="Wjwc4006", Encrypt="yes", TrustServerCertificate="no", ConnectionTimeout=30).cursor()

def readFromDb(dbQuery):
    conn.execute(dbQuery)
    return conn.fetchone()

def readAllFromDb(dbQuery):
    conn.execute(dbQuery)
    return conn.fetchall()

def insertUpdateDeleteToDb(dbQuery):
    conn.execute(dbQuery)
    result = conn.rowcount
    conn.commit()
    return result

def insertUpdateBookToDb(dbQuery, bindata):
    param = (db.Binary(bindata))
    conn.execute(dbQuery, param)
    result = conn.rowcount
    conn.commit()
    return result