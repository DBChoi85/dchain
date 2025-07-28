import sqlite3
import os

class Toekn_List:
    def __init__(self):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "token_list.db")
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS kv (
                                key INTEGER PRIMARY KEY AUTOINCREMENT,
                                addr TEXT NOT NULL,
                                token_name TEXT,
                                token_symbol TEXT,
                                contract_addr TEXT UNIQUE,
                                issued TEXT,
                                meta_data TEXT
                            )
                            """
                            )
        
    def close(self):
        self.conn.commit()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()
    
    def set_token(self, addr, token_name, token_symbol, contract_addr, issued, meta_data):
        try:
            self.cursor.execute("""
                            INSERT INTO kv (addr, token_name, token_symbol, contract_addr, issued, meta_data) VALUES(?, ?, ?, ?, ?, ?)
                            """, (addr, token_name, token_symbol, contract_addr, issued, meta_data))
        except:
            print(f"이미 존재하는 토큰입니다 : {token_name, contract_addr}")

