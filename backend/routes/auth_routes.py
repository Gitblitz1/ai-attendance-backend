from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import SessionLocal
from models.user_model import User
import uuid

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email'); password = data.get('password')
    if not email or not password:
        return jsonify({'ok':False, 'message':'email and password required'}), 400
    db = SessionLocal()
    try:
        existing = db.query(User).filter((User.email==email)|(User.uid==email)).first()
        if existing:
            return jsonify({'ok':False, 'message':'User exists'}), 400
        uid = str(uuid.uuid4())
        user = User(uid=uid, email=email, hashed_password=generate_password_hash(password))
        db.add(user); db.commit()
        return jsonify({'ok':True, 'uid': uid, 'message':'Registered'})
    finally:
        db.close()

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email'); password = data.get('password')
    if not email or not password:
        return jsonify({'ok':False, 'message':'email and password required'}), 400
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email==email).first()
        if not user or not check_password_hash(user.hashed_password, password):
            return jsonify({'ok':False, 'message':'Invalid credentials'}), 401
        return jsonify({'ok':True, 'uid': user.uid, 'email': user.email})
    finally:
        db.close()
