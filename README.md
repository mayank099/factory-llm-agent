## Steps for set up

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## For Freezing the requirements
pip freeze > requirements.txt


python run.py

## NGROK
ngrok.exe http 5001 --domain enjoyed-slowly-cowbird.ngrok-free.app


pip freeze > requirements.txt


## To do ssh inside the container
sudo docker exec -it b9b6394eae60 /bin/bash