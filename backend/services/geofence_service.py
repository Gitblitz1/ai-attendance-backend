import math
from config import GEOFENCE_CENTER_LAT, GEOFENCE_CENTER_LNG, GEOFENCE_RADIUS_M

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1); dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def check_inside(lat, lng):
    lat = float(lat); lng = float(lng)
    dist = haversine_m(lat, lng, GEOFENCE_CENTER_LAT, GEOFENCE_CENTER_LNG)
    return {
        'ok': dist <= GEOFENCE_RADIUS_M,
        'distance_m': round(dist,2),
        'center': {'lat': GEOFENCE_CENTER_LAT, 'lng': GEOFENCE_CENTER_LNG},
        'radius_m': GEOFENCE_RADIUS_M
    }
