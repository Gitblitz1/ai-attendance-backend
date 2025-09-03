import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get("PORT", 5000))
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
GEOFENCE_CENTER_LAT = float(os.environ.get("GEOFENCE_CENTER_LAT", "28.6139"))
GEOFENCE_CENTER_LNG = float(os.environ.get("GEOFENCE_CENTER_LNG", "77.2090"))
GEOFENCE_RADIUS_M = float(os.environ.get("GEOFENCE_RADIUS_M", "150"))
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///attendance.db")
STORAGE_ROOT = os.environ.get("STORAGE_ROOT", "storage/faces")
