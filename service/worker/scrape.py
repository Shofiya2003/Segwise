import gspread
import pandas as pd

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
    df = pd.DataFrame(data)
    return df

# Example usage:
if __name__ == "__main__":
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ShbFMzRUuIJY8amTA58UuEHwsc3UmAnd_LzduBwcBhE/edit?gid=1439814054#gid=1439814054' 
    df = scrape_public_google_sheet(spreadsheet_url)
    print(df.head())
