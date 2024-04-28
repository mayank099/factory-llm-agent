# app/__init__.py
from flask import Flask, request, abort
from config import Config
from pymongo import MongoClient
import logging.config
from app.log_config import LOGGING_CONFIG
from flask_cors import CORS  # Import the CORS object

# Initialize logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)  # get a logger instance

app = Flask(__name__)
CORS(app)  # Enable CORS on the app, with default options allowing all origins

app.config.from_object(Config)
print(app.config['MONGO_URI'])
mongo = MongoClient(app.config['MONGO_URI'])

logger.info(f"APP Initialized :: Happy Hunting :::::")

from app.routes import user