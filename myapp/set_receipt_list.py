import sqlite3
import os
import json

class Receipt_List:
    def __init__(self):
        self.conn = None

    def connect(self, cont_addr):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "{}_receipt.db".format(cont_addr))
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS kv (
                                key INTEGER PRIMARY KEY AUTOINCREMENT,
                                contract_addr TEXT,
                                issued TEXT,
                                sender TEXT,
                                receiver TEXT,
                                amount INTEGER,
                                meta_data TEXT
                            )
                            """
                            )
        
    def close(self):
        self.conn.commit()
        self.conn.close()

    def commit(self):
        self.conn.commit()
    
    def set_receipt(self, cont_addr, issued, sender, receiver, amount, meta_Data):
        try:
            self.cursor.execute("INSERT INTO kv (contract_addr, issued, sender, receiver, amount, meta_data) VALUES(?, ?, ?, ?, ?, ?)", (cont_addr, issued, sender, receiver, amount, json.dumps(meta_Data)))
        except Exception as e:
            print(f'잔액 기록 실패 : {e}')