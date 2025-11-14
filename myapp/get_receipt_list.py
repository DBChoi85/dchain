import sqlite3
import os
import json

class Read_MeataData:
    def __init__(self):
        self.conn = None

    def connect(self, cont_addr):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "{}_receipt.db".format(cont_addr))
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    
    def all_list(self):
        self.cursor.execute("SELECT * FROM kv")
        rows = self.cursor.fetchall()

        # meta_data는 JSON 문자열이므로 Python 객체로 변환
        result = []
        for row in rows:
            result.append({
                "key": row[0],
                "contract_addr": row[1],
                "issued": row[2],
                "sender": row[3],
                "receiver": row[4],
                "amount": row[5],
                "meta_data": json.loads(row[6]) if row[6] else None
            })
        return result

    def get_meta_data(self, key):
        self.cursor.execute("""
                            SELECT meta_data FROM kv WHERE key = ?
                            """,(key))
        return(self.cursor.fetchone()[0])
    
