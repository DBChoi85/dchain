import sqlite3
import os

class Balance_List:
    def __init__(self):
        self.conn = None

    def connect(self, db_name):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "{}.db".format(db_name))
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def all_list(self):
        self.cursor.execute("SELECT address, value FROM kv")
        return self.cursor.fetchall()
        

    def get_balance(self, address):
        try:
            self.cursor.execute("SELECT value FROM kv WHERE address = ?",(address,))
            return(self.cursor.fetchone()[0])
        except:
            return False

if __name__ == "__main__":
    db = Balance_List()
    print(db.all_list())
    addr = '0xD1c8163FC4CE4fd1498E21368694dD3B296316CDfca'
    print(type(db.get_balance(addr)))