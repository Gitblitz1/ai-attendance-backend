import os, base64
from datetime import datetime
from pathlib import Path
from config import STORAGE_ROOT

def save_dataurl_png(uid: str, dataurl: str) -> str:
    if ',' not in dataurl:
        raise ValueError('Invalid data URL')
    header, b64 = dataurl.split(',',1)
    if 'base64' not in header:
        raise ValueError('Unsupported image encoding')
    raw = base64.b64decode(b64)
    user_dir = Path(STORAGE_ROOT) / uid
    user_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    path = user_dir / f"{ts}.png"
    with open(path, 'wb') as f:
        f.write(raw)
    return str(path)
