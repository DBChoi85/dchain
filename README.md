# dchain

## 환경 구성
python 3.11 이상 필요  
방화벽에서 접속 port 개방 필요

1. git clone
```
git clone https://github.com/DBChoi85/dchain.git
```
or
```
gh repo clone dbchoi85/dchain
```
2. Dependency install
```
pip install -r requirements.txt
```
접속 port 변경 시 run.py 수정
```
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000, debug=True)
```
host = '0.0.0.0' -> 모든 네트워크 인터페이스, 고정 IP로 설정을 원할 시 해당 IP로 변경  
port = 5000 -> 접속 port, 변경 필요시 해당 port 입력
## 실행
```
python run.py
```



## 각종 DB 및 DID 생성 위치.
