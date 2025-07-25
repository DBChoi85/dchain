import sqlite3
# import hashlib
import json

class KeyValueDB:
    def __init__(self):
        self.conn = sqlite3.connect('mySqlite.db')
        self.cursor = self.conn.cursor()

    def keyValueTable(self):
        #if not exit
        self.cursor.execute("CREATE TABLE keyValue(key BLOB PRIMARY KEY, value BLOB);")

    def close(self):
        self.conn.commit()
        self.conn.close()

    def get(self, key):
        self.cursor.execute("SELECT value FROM keyValue WHERE key = ?", (key,))
        return self.cursor.fetchone()[0]
    
    def getAll(self):
        self.cursor.execute("SELECT key, value FROM keyValue")
        # self.cursor.fetchmany(num)
        return self.cursor.fetchall()

    def set(self, key, value):
        # self.cursor.execute("INSERT INTO keyValue (key, value) VALUES (?, ?)", (key, value))
        # if already exist
        # self.cursor.execute("UPDATE keyValue SET value = ? WHERE key = ?", (value, key))
        self.cursor.execute("""
                    INSERT INTO keyValue (key, value) VALUES (?, ?)
                    ON CONFLICT(key) 
                    DO UPDATE SET value = excluded.value""", (key, value))
        # self.cursor.execute("REPLACE INTO kv_store (key, value) VALUES (?, ?)", (key, value)
    def setMany(self, keyValues):
        self.cursor.executemany("INSERT INTO keyValue VALUES(?, ?)", keyValues)
        self.conn.commit()

    def remove(self, key):
        self.cursor.execute("DELETE FROM keyValue WHERE key = ?", (key,))

if __name__ == '__main__':
    db = KeyValueDB()
    #
    # db.keyValueTable()
    db.set(b"data1", b"json{data1}")
    #
#    key = hashlib.sha256(b"data2").digest()
    key = b"data2"
    jsonData = {
        '@context': 'https://www.w3.org/',
        'id': 'did:aiia:0001',
        'keys': [{'id':'abc123','type':'x'}, {'id':'def357','controller':'abc357'}, {'controller':'c12','type':'Normal'}]
    }
    value = json.dumps(jsonData)

    db.set(key, value)
#    returnValue = db.get(hashlib.sha256(b"data1").digest())
    returnValue = db.get(b"data1")
    print(returnValue.decode())
    print(json.loads(db.get(key)))
    db.set(key, b"json{newData}")
    # print(db.getAll())
    for key, value in db.getAll():
        print(f'{key.decode()}: {value.decode()}')
    db.close()