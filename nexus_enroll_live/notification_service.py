# notification_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    # In a real system, this would send an email or push notification.
    # Here, we just print to the console to show it was called.
    print(f"\n--- 📧 NOTIFICATION SENT 📧 ---")
    print(f"TO: {data['user_name']} ({data['user_id']})")
    print(f"MESSAGE: {data['message']}")
    print("-----------------------------\n")
    return jsonify({"status": "Notification processed"}), 200

if __name__ == '__main__':
    # Runs on port 5003
    app.run(port=5003, debug=True)