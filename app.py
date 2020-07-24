#!/usr/bin/env python3

import os
import sys

from flask import Flask
from flask_jwt_extended import JWTManager

# Set start dirs
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Other imports
from core import MainConfig, Initialization
from controllers import MainController

# Initialization
config = MainConfig()
Initialization.database_initialization()
app = Flask(__name__)
app.secret_key = config.secret_key.encode()
jwt = JWTManager(app)

# Rules mapping
app.add_url_rule('/api/registration/', 'registration', MainController.registration, methods=['POST'])
app.add_url_rule('/api/login/', 'login', MainController.login, methods=['POST'])
app.add_url_rule('/api/create_post/', 'create_post', MainController.create_post, methods=['POST'])
app.add_url_rule('/api/like_post/', 'like_post', MainController.like_post, methods=['POST'])
app.add_url_rule('/api/unlike_post/', 'unlike_post', MainController.unlike_post, methods=['POST'])
app.add_url_rule('/api/user_activity/<int:user_id>', 'user_activity', MainController.user_activity, methods=['GET'])
app.add_url_rule('/api/analytics/from/<string:date_from>/to/<string:date_to>', 'analytics', MainController.analytics,
                 methods=['GET'])


if __name__ == '__main__':
    app.run(host=config.server_host, port=int(config.server_port))
