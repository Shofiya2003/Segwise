
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
    try:
        params = request.args
        query = session.query(Game)
        aggregate_results = {}
        for key, value in params.items():
            if hasattr(Game, key):
                column = getattr(Game, key)
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
                    if key=="name":
                        print(value)
                        query = query.filter(column.like(f'{value}%'))
                        continue
                    query = query.filter(column.like(f'%{value}%'))
    
            elif key in ['sum', 'max', 'min', 'avg']:
                print(value)
                if hasattr(Game, value):
                    func_column = getattr(Game, value)
                    if func_column.type.python_type == int or func_column.type.python_type == float:
                        if key == 'sum':
                            result = session.query(func.sum(func_column)).scalar()
                        elif key == 'max':
                            result = session.query(func.max(func_column)).scalar()
                        elif key == 'min':
                            result = session.query(func.min(func_column)).scalar()
                        elif key == 'avg':
                            result = session.query(func.avg(func_column)).scalar()
                        aggregate_results[f"{key}_{func_column}"] = result
                    else:
                        return json.jsonify({"msg": "Aggrgate function can be applied to only Integer or Float columns "}) , 400
                else:
                    return json.jsonify({"msg": f"Attribute {value} not present"}), 400
            else:
                return json.jsonify({"msg": f"Attribute {key} not present"}), 400
                
        results = query.all()
        if len(aggregate_results.keys()) != 0:
            return json.jsonify({"games":[game.to_dict() for game in results],"aggregate_results":aggregate_results}) , 200
        else:
            return json.jsonify({"games":[game.to_dict() for game in results]}) , 200
    except AttributeError as e:
        return json.jsonify({"msg":"Attribute missing in "})
    except Exception as e:
        return json.jsonify({"msg": "Something went wrong"}), 500