# config.py
import os
from dotenv import load_dotenv

# Determine which .env file to load based on the FLASK_ENV value
environment = os.getenv('FLASK_ENV', '')
dotenv_path = ".env"
if environment:
    dotenv_path = f'.env.{environment}'

print(f"Initializing the environment for Our Application Env :: {dotenv_path}")

# Load the .env file
load_dotenv(dotenv_path)

class Config:
    MONGO_URI = os.getenv('MONGO_URI') or "mongodb+srv://<username>:ul1Zb7zly1GLGX0P@agentcluster.gu1bq8e.mongodb.net/?retryWrites=true&w=majority&appName=AgentCluster"
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True