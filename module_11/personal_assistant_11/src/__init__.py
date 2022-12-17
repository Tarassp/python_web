from flask import Flask
from config import config

app = Flask(__name__)
app.debug = True
app.config.from_object(config.Config)

from src import routes