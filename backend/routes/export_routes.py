from flask import Blueprint, request, jsonify, Response
from database.db import SessionLocal
from models.attendance_model import Attendance
import csv, io

bp = Blueprint('export', __name__)

@bp.route('/', methods=['GET'])
def export():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({'ok':False, 'message':'uid required'}), 400
    db = SessionLocal()
    try:
        rows = db.query(Attendance).filter(Attendance.uid==uid).order_by(Attendance.date.desc()).all()
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(['id','uid','date','time','lat','lng','status'])
        for r in rows:
            writer.writerow([r.id, r.uid, r.date, r.time, r.lat, r.lng, r.status])
        output = si.getvalue()
        return Response(output, mimetype='text/csv', headers={'Content-Disposition':f'attachment; filename=attendance_{uid}.csv'})
    finally:
        db.close()
