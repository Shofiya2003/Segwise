
from flask import Blueprint,Response,request,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import traceback
from src.database import Game, get_engine
from sqlalchemy.orm import Session
from sqlalchemy import func
game = Blueprint('games',__name__)

engine = get_engine()
session = Session(engine)

@game.route('/', methods=['GET'])
@jwt_required()
def query():
    params = request.args
    query = session.query(Game)
    
    for key, value in params.items():
        if hasattr(Game, key):
            column = getattr(Game, key)
            print(column.type.python_type)
            if column.type.python_type == int or column.type.python_type == float:
                if value.startswith('>'):
                    query = query.filter(column > float(value[1:]))
                elif value.startswith('<'):
                    query = query.filter(column < float(value[1:]))
                else:
                    query = query.filter(column == float(value))
            elif column.type.python_type == bool:
                query = query.filter(column == (value.lower() == 'true'))
            elif column.type.python_type == datetime.date:
                if value.startswith('>'):
                    query = query.filter(column > datetime.datetime.strptime(value[1:], '%Y-%m-%d').date())
                elif value.startswith('<'):
                    query = query.filter(column < datetime.datetime.strptime(value[1:], '%Y-%m-%d').date())
                else:
                    query = query.filter(column == datetime.datetime.strptime(value, '%Y-%m-%d').date())
            else:
                query = query.filter(column.like(f'%{value}%'))

        elif key in ['sum', 'max', 'min', 'avg']:
            func_column = getattr(Game, value)
            if key == 'sum':
                result = session.query(func.sum(func_column)).scalar()
            elif key == 'max':
                result = session.query(func.max(func_column)).scalar()
            elif key == 'min':
                result = session.query(func.min(func_column)).scalar()
            elif key == 'avg':
                result = session.query(func.avg(func_column)).scalar()
            return json.jsonify({key: result})
    
    results = query.all()
    return json.jsonify([game.to_dict() for game in results])