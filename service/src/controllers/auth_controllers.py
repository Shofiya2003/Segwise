from flask import request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt
import datetime
from src.database import User, get_engine
from sqlalchemy.orm import Session

auth = Blueprint('auth',__name__)

engine = get_engine()
session = Session(engine)

# Register endpoint (for creating new users)
@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    if session.query(User).filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    salt = bcrypt.gensalt() 
    hashPassword = bcrypt.hashpw(password.encode('utf-8'), salt) 
    new_user = User(username=username, password=hashPassword)
    session.add(new_user)
    session.commit()
    return jsonify({"msg": "User created successfully"}), 201

# Login endpoint
@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    user = session.query(User).filter_by(username=username).first()
    password = password.encode('utf-8')
    if not user or not bcrypt.checkpw(password, user.password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=60))
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Refresh token endpoint
@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
