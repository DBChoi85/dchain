import sqlite3
import os

class Acc_List:
    def __init__(self):
        db_dir_loc = "./data_base"
        db_loc = os.path.join(db_dir_loc, "token_list.db")
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def all_list(self):
        self.cursor.execute("SELECT token_name, contract_addr, issued, supply FROM kv")
        tmp_list = self.cursor.fetchall()
        return tmp_list


if __name__ == "__main__":
    db = Acc_List()
    print(db.all_list())