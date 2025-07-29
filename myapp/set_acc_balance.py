import sqlite3
import os

class Balance_List:
    def __init__(self):
        self.conn = None

    def connect(self, cont_addr):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "{}.db".format(cont_addr))
        self.conn = sqlite3.connect(db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS kv (
                                address TEXT PRIMARY KEY,
                                value INTEGER
                            )
                            """
                            )
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    def commit(self):
        self.conn.commit()
    
    def set_balance(self, address, balance):
        try:
            self.cursor.execute("INSERT INTO kv (address, value) VALUES(?, ?)", (address, balance))
        except Exception as e:
            print(f'잔액 기록 실패 : {address} - {e}')
        
    def increase_balance(self, address, amount):
        try:
            self.cursor.execute("SELECT value FROM kv WHERE address = ?", (address,))
            row = self.cursor.fetchone()
            if row:
                new_balance = row[0] + amount
                self.cursor.execute("UPDATE kv SET value = ? WHERE address = ?", (new_balance, address))
            else:
                self.cursor.execute("INSERT INTO kv (address, value) VALUES (?, ?)", (address, amount))
        except Exception as e:
            print(f'잔액 증가 실패: {address} - {e}')

    def decrease_balance(self, address, amount):
        try:
            self.cursor.execute("SELECT value FROM kv WHERE address = ?", (address,))
            row = self.cursor.fetchone()
            if row:
                if row[0] >= amount:
                    new_balance = row[0] - amount
                    self.cursor.execute("UPDATE kv SET value = ? WHERE address = ?", (new_balance, address))
                else:
                    print(f"잔액 부족: {address} (현재 잔액 {row[0]}, 요청 감소 {amount})")
            else:
                print(f"주소 없음: {address}")
        except Exception as e:
            print(f'잔액 감소 실패: {address} - {e}')


if __name__ == "__main__":
    data = {'state': 'OK', 
        'rcode': {}, 'msg': '', 
        'data': 
        {'key_pair': {'privatekey': '288d7611880f95c78d0c71358d94a3871cc90f79317061b986f9ea609e4f7a45fpr', 
                    'publickey': '0220fbd51c70ec85758bb4a0f0b838aaff0ed4ce63cce26d6e62a4cc4858248090fpu', 
                    'address': '0xD1c8163FC4CE4fd1498E21368694dD3B296316CDfca'}}, 
                    'cid': 'c9a1869d9080e8732eda0228e3984f18df7cf657b574ce7de1b7bfb61362d4b8'}

    key_pair = data['data']['key_pair']
    addr = key_pair['address']
    cid = key_pair['publickey']
    pkey = key_pair['privatekey']

    db = Balance_List()
    db.connect(pkey)
    db.set_balance(addr, 10)
    db.commit()
    db.increase_balance('test', 20)
    db.commit()