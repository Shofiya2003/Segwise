import gspread
import pandas as pd
from sqlalchemy.orm import Session
from src.services.game_service import insert_game

def scrape_public_google_sheet(spreadsheet_url):
    """
    Scrapes data from a public Google Sheet and returns it as a Pandas DataFrame.

    Parameters:
    - spreadsheet_url: str, the URL of the Google Sheet

    Returns:
    - df: DataFrame containing the scraped data
    """
    gc = gspread.service_account()
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.sheet1
    data = worksheet.get_all_records()
    # df = pd.DataFrame(data)
    for game in data:
        success, message = insert_game(game)
        if not success:
            print(message)
            return
    print("Successfully inserted all records")
