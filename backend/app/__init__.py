from flask import Flask
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app,origins="*")

from app import routes
