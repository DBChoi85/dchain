import sqlite3
import os

class Acc_List:
    def __init__(self):
        db_dir_loc = "./data_base"
        db_loc = os.path.join(db_dir_loc, "user_acc_list.db")
        self.conn = sqlite3.connect(db_loc)
        self.cursor = self.conn.cursor()

    def all_list(self):
        self.cursor.execute("SELECT address FROM kv")
        tmp_list = self.cursor.fetchall()
        tmp_list = [x[0] for x in tmp_list]
        tmp_list = list(set(tmp_list))
        return tmp_list

    def get_public_key(self, address):
        key_type = 'public'
        self.cursor.execute("""
                            SELECT value FROM kv WHERE address = ? AND type = ?
                            """,(address, key_type))
        return(self.cursor.fetchone()[0])

    def get_private_key(self, address):
        key_type = 'private'
        self.cursor.execute("""
                            SELECT value FROM kv WHERE address = ? AND type = ?
                            """,(address, key_type))
        return(self.cursor.fetchone()[0])



if __name__ == "__main__":
    db = Acc_List()
    print(db.all_list())