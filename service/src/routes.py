from flask import Blueprint, Request, Response, json
from  src.controllers.csv_upload_controllers import upload_csv
from src.controllers.game_controllers import game
from src.controllers.auth_controllers import auth
api = Blueprint('api',__name__)

api.register_blueprint(upload_csv,url_prefix='/upload_csv')
api.register_blueprint(game,url_prefix='/games')
api.register_blueprint(auth, url_prefix='/auth')