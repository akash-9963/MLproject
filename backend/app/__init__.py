from flask import Flask
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app,origins="https://ml-project-red.vercel.app")

from app import routes
