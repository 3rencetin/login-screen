from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

# Örnek kullanıcı veritabanı
registered_users = {
    "00:1B:44:11:3A:B7": "Registered User 1"
}

@app.route('/check', methods=['POST'])
def check_user():
    data = request.json
    mac_id = data.get("mac_id")
    ip = request.remote_addr

    if mac_id in registered_users:
        return jsonify({"status": "registered", "user": registered_users[mac_id]})
    else:
        return jsonify({"status": "unregistered", "message": "Unauthorized use detected!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

