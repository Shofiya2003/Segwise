
from flask import json
from flask import Flask
import os
from .config.config import Config
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from waitress import serve

load_dotenv()
app = Flask(__name__)
config = Config().dev_config
app.env = config.ENV

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix = "/api")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

if __name__ == "__main__":
    # create a ping route
    @app.route('/',methods=['GET'])
    def pingServer():
        return json.jsonify({"msg":"we are logically blessed"})
    print("Starting the app at 5000")
    serve(app, host='0.0.0.0', port=5000)