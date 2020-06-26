run: run-server run-front run-documentation

install:
	cd ./server && python3.6 -m pip install -r requirements.txt
	cd ./front && npm install
	npm i docsify-cli -g

run-server:
	cd ./server && python3.6 app.py &

run-front:
	cd ./front && npm run serve &

run-documentation:
	docsify serve ./docs