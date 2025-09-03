from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import io
import os
from datetime import datetime
try:
    import xlsxwriter
except Exception:
    xlsxwriter = None

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "msg": "Backend up"}), 200

@app.post("/api/attendance/enroll")
def enroll():
    data = request.get_json() or {}
    if not data.get("image"):
        return jsonify({"error": "image required"}), 400
    # In a real app you would persist the image; we just ACK
    return jsonify({"ok": True, "message": "Face enrolled"}), 200

@app.post("/api/attendance/mark")
def mark():
    data = request.get_json() or {}
    if not data.get("image"):
        return jsonify({"error": "image required"}), 400
    now = datetime.utcnow().isoformat() + "Z"
    return jsonify({"ok": True, "message": f"Attendance marked at {now}"}), 200

@app.get("/api/export/xlsx")
def export_xlsx():
    # Generate a tiny XLSX in-memory
    if xlsxwriter is None:
        return jsonify({"error": "xlsxwriter not installed on server"}), 500
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {'in_memory': True})
    ws = wb.add_worksheet("Attendance")
    ws.write_row(0, 0, ["Name", "Email", "Timestamp"])
    ws.write_row(1, 0, ["User", "user@example.com", datetime.utcnow().isoformat()+"Z"])
    wb.close()
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="attendance.xlsx")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
