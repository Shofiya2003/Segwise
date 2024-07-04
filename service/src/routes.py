from flask import Blueprint, Request, Response, json
from  src.controllers.csv_upload_controller  import upload_csv
from src.controllers.game_controllers import game
api = Blueprint('api',__name__)

api.register_blueprint(upload_csv,url_prefix='/upload_csv')
api.register_blueprint(game,url_prefix='/games')