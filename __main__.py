#!/usr/bin/env python3

import os
import sys

from flask import Flask

# Set start dirs
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Other imports
from core import MainConfig, Initialization
from controllers import MainController

# Initialization
Initialization.start_initialization()
app = Flask(__name__)

# Routes mapping
app.add_url_rule('/api/registration/', 'registration', MainController.registration, methods=['POST'])
app.add_url_rule('/api/login/', 'login', MainController.login, methods=['POST'])


if __name__ == '__main__':
    config = MainConfig()
    app.run(host=config.server_host, port=int(config.server_port))
