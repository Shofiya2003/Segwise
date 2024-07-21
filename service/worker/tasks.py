import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.services.game_service import insert_game
from src.database import UploadLogs, get_engine, Game
from sqlalchemy.orm import Session
from .celery import app
from celery.utils.log import get_task_logger
from pathlib import Path
from sentry_sdk import capture_exception
engine = get_engine()
session = Session(engine)

logger = get_task_logger(__name__)

creds = ServiceAccountCredentials.from_json_keyfile_name(Path("./worker/service_account.json"))

@app.task
def scrape_public_google_sheet(spreadsheet_url,upload_log_id):
    logger.info("Uploading data from the CSV file")
    try:
        # gc = gspread.service_account()
        gc = gspread.authorize(creds)
        sh = gc.open_by_url(spreadsheet_url)
        worksheet = sh.sheet1
        data = worksheet.get_all_records()
        session.begin()
        new_games = []
        for game in data:
            game, message = insert_game(game, upload_log_id)
            if not game:
                logger.info("Something went wrong")
                logger.error(message)
                capture_exception(message)
                continue
            new_games.append(game)
        session.bulk_insert_mappings(Game, new_games)
        session.commit()
        upload_log = session.query(UploadLogs).filter(UploadLogs.id == upload_log_id).one()
        upload_log.success = True
        session.commit()
        logger.info("Successfully inserted all records")
    except Exception as e:
        session.rollback()
        print(e)
        capture_exception(e)

