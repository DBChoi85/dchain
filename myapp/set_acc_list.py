import sqlite3
import os

class Acc_List:
    def __init__(self):
        db_dir_loc = "./data_base"
        if not os.path.exists(db_dir_loc):
            os.mkdir(db_dir_loc)
        db_loc = os.path.join(db_dir_loc, "user_acc_list.db")
        self.conn = sqlite3.connect(db_loc)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS kv (
                                address TEXT,
                                type TEXT CHECK(type IN ('public', 'private')),
                                value TEXT,
                                PRIMARY KEY (address, type)
                            )
                            """
                            )
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def save_private_key(self, address, key_value):
        try:
            key_type = 'private'
            self.cursor.execute("""
                                INSERT INTO kv (address, type, value) VALUES (?, ?, ?)
                                """, (address, key_type, key_value))
        except:
            print(f"이미 존재하는 지갑입니다 : {address}")
    
    def save_public_key(self, address, key_value):
        try:
            key_type = 'public'
            self.cursor.execute("""
                                INSERT INTO kv (address, type, value) VALUES (?, ?, ?)
                                """, (address, key_type, key_value))
        except:
            print(f"이미 존재하는 지갑입니다 : {address}")

    def remove(self, address):
        self.cursor.execute("DELETE FROM kv WHERE key = ?", (address,))

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
    public_key = key_pair['publickey']
    private_key = key_pair['privatekey']

    db = Acc_List()
    db.save_private_key(addr, private_key)
    db.save_public_key(addr, public_key)
    db.commit()
