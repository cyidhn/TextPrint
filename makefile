run: run-server run-front

run-server:
	cd ./server && python3.6 app.py &

run-front:
	cd ./front && npm run serve