import gspread
from src.services.game_service import insert_game
from src.database import UploadLogs, get_engine
from sqlalchemy.orm import Session
from .celery import app
from celery.utils.log import get_task_logger

engine = get_engine()
session = Session(engine)

logger = get_task_logger(__name__)

@app.task
def scrape_public_google_sheet(spreadsheet_url,upload_log_id):
    """
    Scrapes data from a public Google Sheet and saves it in db.

    Parameters:
    - spreadsheet_url: str, the URL of the Google Sheet
    - upload_log_id: integer, the id of the upload log
    """
    logger.info("Uploading data from the CSV file")
    gc = gspread.service_account()
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.sheet1
    data = worksheet.get_all_records()
    for game in data:
        success, message = insert_game(game, upload_log_id)
        if not success:
            logger.info("Something went wrong")
            logger.error(message)
            raise Exception("scraping failed")
    upload_log = session.query(UploadLogs).filter(UploadLogs.id == upload_log_id).one()
    upload_log.success = True
    session.commit()
    logger.info("Successfully inserted all records")

