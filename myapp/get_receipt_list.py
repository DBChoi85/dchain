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
        self.cursor.execute("SELECT address FROM kv")
        tmp_list = self.cursor.fetchall()
        tmp_list = [x[0] for x in tmp_list]
        tmp_list = list(set(tmp_list))
        return tmp_list

    def get_meta_data(self, key):
        self.cursor.execute("""
                            SELECT meta_data FROM kv WHERE key = ?
                            """,(key))
        return(self.cursor.fetchone()[0])
    
