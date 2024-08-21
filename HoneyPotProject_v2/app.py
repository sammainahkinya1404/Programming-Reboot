from flask import Flask, render_template, jsonify
from models import LogEntry, db_session
import threading
from sniffer import start_sniffing
from log_monitor import start_monitoring

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def get_logs():
    logs = db_session.query(LogEntry).all()
    log_list = [{'id': log.id, 'type': log.log_type, 'message': log.message} for log in logs]
    return jsonify(log_list)

if __name__ == '__main__':
    threading.Thread(target=start_sniffing).start()
    threading.Thread(target=start_monitoring).start()
    app.run(debug=True)
