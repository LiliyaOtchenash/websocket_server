# 
## install in
pip install -r requirements.txt
## change directory
cd currency_quotes/quotes
## Run server script
python manage.py websocket_client.py
## Run producer script
python manage.py websocket_producer.py
## Run client script 
(every script is one client, run it several times if you have several clients)
python manage.py websocket_server.py