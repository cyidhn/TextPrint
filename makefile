run: run-server run-front

install:
	cd ./server && python3.6 -m pip install -r requirements.txt
	cd ./front && npm install

run-server:
	cd ./server && python3.6 app.py &

run-front:
	cd ./front && npm run serve