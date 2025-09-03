from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from models.attendance_model import Attendance
from services.image_service import save_dataurl_png
from services.geofence_service import check_inside
from datetime import datetime, timezone

bp = Blueprint('attendance', __name__)

@bp.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json() or {}
    uid = data.get('uid'); image = data.get('image')
    if not uid or not image:
        return jsonify({'ok':False, 'message':'uid or image missing'}), 400
    try:
        path = save_dataurl_png(uid, image)
    except Exception as e:
        return jsonify({'ok':False, 'message': f'Invalid image: {e}'}), 400
    # here you could create enrollment record - demo skip
    return jsonify({'ok':True, 'message':'Enrolled', 'path': path})

@bp.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json() or {}
    uid = data.get('uid'); image = data.get('image')
    lat = data.get('lat'); lng = data.get('lng')
    if not uid or not image:
        return jsonify({'ok':False, 'message':'uid or image missing'}), 400
    # geofence check
    if lat is not None and lng is not None:
        geo = check_inside(lat, lng)
        if not geo['ok']:
            return jsonify({'ok':False, 'message':'Outside geofence','geo':geo}), 403
    # date/time
    now = datetime.now(timezone.utc)
    date = now.strftime('%Y-%m-%d'); time = now.strftime('%H:%M:%S')
    db = SessionLocal()
    try:
        # duplicate check
        existing = db.query(Attendance).filter(Attendance.uid==uid, Attendance.date==date).first()
        if existing:
            return jsonify({'ok':True, 'message':'Attendance already marked for today.'})
        # save image
        try:
            save_dataurl_png(uid, image)
        except Exception as e:
            return jsonify({'ok':False, 'message': f'Invalid image: {e}'}), 400
        rec = Attendance(uid=uid, date=date, time=time, lat=lat, lng=lng, status='Present')
        db.add(rec); db.commit()
        return jsonify({'ok':True, 'message':'Attendance marked', 'date':date, 'time':time})
    finally:
        db.close()

@bp.route('/<uid>', methods=['GET'])
def list_attendance(uid):
    db = SessionLocal()
    try:
        rows = db.query(Attendance).filter(Attendance.uid==uid).order_by(Attendance.date.desc(), Attendance.time.desc()).all()
        out = []
        for r in rows:
            out.append({'id': r.id, 'uid': r.uid, 'date': r.date, 'time': r.time, 'lat': r.lat, 'lng': r.lng, 'status': r.status})
        return jsonify(out)
    finally:
        db.close()
