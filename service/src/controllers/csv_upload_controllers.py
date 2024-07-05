from flask import Blueprint,Response,request,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import traceback
from worker.scrape import scrape_public_google_sheet
upload_csv = Blueprint('upload_csv',__name__)

@jwt_required
@upload_csv.route('/',methods=['POST'])
def handle_upload():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or not 'csv_url' in data:
        return json.jsonify({"error": "Invalid input"}), 400
    try:
        scrape_public_google_sheet(data['csv_url'])
        return json.jsonify({"message": "CSV file uploaded"}), 200
    except Exception as e:
        print(e)
        return json.jsonify({"error": f"Internal server error: {str(e)}"}), 500
