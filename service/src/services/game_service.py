from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.database import Game, Base, engine
from datetime import datetime
import ast

def insert_game(data, upload_log_id):
    # Parse data and insert into database
    session = sessionmaker(bind=engine)()

    releaseDate = parse_date(data.get('Release date', None))
    supported_languges = data.get('Supported languages', '')
    data_list = ast.literal_eval(supported_languges)
    print(data_list)
    if isinstance(data_list, list):
        supported_languges = ','.join(data_list)
    
    try:
        game = Game(
            appId=int(data.get('AppID', 0)),
            name=data.get('Name', ''),
            releaseDate=releaseDate,
            requiredAge=int(data.get('Required age', 0)),
            price=float(data.get('Price', 0.0)),
            dlcCount=int(data.get('DLC count', 0)),
            aboutTheGame=data.get('About the game', ''),
            supportedLanguages=supported_languges,
            windows=bool(data.get('Windows', 'FALSE').upper() == 'TRUE'),
            linux=bool(data.get('Linux', 'FALSE').upper() == 'TRUE'),
            mac=bool(data.get('Mac', 'FALSE').upper() == 'TRUE'),
            positive=int(data.get('Positive', 0)),
            negative=int(data.get('Negative', 0)),
            scoreRank=int(data.get('Score rank', 0)) if data.get('Score rank') else None,
            developers=data.get('Developers', ''),
            publishers=data.get('Publishers', ''),
            categories=data.get('Categories', ''),
            genres=data.get('Genres', ''),
            tags=data.get('Tags', ''),
            upload_log_id=upload_log_id
        )
        
        session.add(game)
        session.commit()
        session.close()
        
        return True, "Game successfully inserted."
    
    except IntegrityError as e:
        session.rollback()
        session.close()
        return False, f"IntegrityError: {str(e)}"
    
    except Exception as e:
        session.rollback()
        session.close()
        return False, f"Error: {str(e)}"
    

def parse_date(date_str):
    formats_to_try = [
        '%b %Y',            # Format like "May 2020"
        '%b %d, %Y'         # Format like "Oct 21, 2008"
    ]

    for date_format in formats_to_try:
        try:
            datetime_object = datetime.strptime(date_str, date_format)
            return datetime_object
        except ValueError:
            continue
    
    raise ValueError(f"Date format not recognized: {date_str}")