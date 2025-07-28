import sqlite3
import os

class Balance_List:
    def __init__(self):
        db_dir_loc = "./data_base"
        db_loc = os.path.join(db_dir_loc, "user_acc_balance.db")
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def all_list(self):
        self.cursor.execute("SELECT address, value FROM kv")
        return self.cursor.fetchall()
        

    def get_balance(self, address):
        self.cursor.execute("SELECT value FROM kv WHERE address = ?",(address,))
        return(self.cursor.fetchone()[0])

if __name__ == "__main__":
    db = Balance_List()
    print(db.all_list())
    addr = '0xD1c8163FC4CE4fd1498E21368694dD3B296316CDfca'
    print(db.get_balance(addr))