from flask import Blueprint,Response,request,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import traceback
from worker.tasks import scrape_public_google_sheet
from src.database import UploadLogs, get_engine
from sqlalchemy.orm import Session

upload_csv = Blueprint('upload_csv',__name__)

engine = get_engine()
session = Session(engine)

@upload_csv.route('/',methods=['POST'])
@jwt_required()
def handle_upload():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or not 'csv_url' in data:
        return json.jsonify({"error": "Invalid input"}), 400
    try:
        prev_upload_log = session.query(UploadLogs).filter(UploadLogs.csv_url == data['csv_url'], UploadLogs.success == True).all()
        if prev_upload_log:
            return json.jsonify({"message":"CSV file already uploaded","log":prev_upload_log}), 200
        uploaded_at = datetime.now()
        new_upload_log = UploadLogs(user_id=current_user, csv_url=data['csv_url'], uploaded_at=uploaded_at)
        session.add(new_upload_log)
        session.commit()
        scrape_public_google_sheet.delay(data['csv_url'], new_upload_log.id)
        return json.jsonify({"message": "Uploading Task Queued"}), 200
    except Exception as e:
        traceback.print_exc(e)
        print(e)
        return json.jsonify({"error": f"Internal server error: {str(e)}"}), 500
