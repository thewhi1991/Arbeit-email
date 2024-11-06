# filepath: /c:/Users/josha/Documents/arbeit/Email_adapter(dev)/backend/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
import json
from email_service import EmailService
from email_receiver import EmailReceiver
from common.logger import Logger
from common.logger import notify_admin  # Import der neuen Funktion
import threading

app = Flask(__name__)

logger = Logger()

# Lade die Konfigurationsdaten aus config.json
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config_data = json.load(f)

@app.route('/configure-email', methods=['POST'])
def configure_email():
    request_data = request.json  # Umbenennen, um Konflikte zu vermeiden
    email_service = EmailService(request_data)
    configuration = email_service.configure_email()
    return jsonify({
        "status": "success",
        "configuration": configuration
    }), 200

@app.route('/test-smtp', methods=['POST'])
def test_smtp():
    request_data = request.json  # Umbenennen, um Konflikte zu vermeiden
    email_service = EmailService(request_data)
    result = email_service.test_smtp_connection()

    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@app.route('/fetch-emails', methods=['POST'])
def fetch_emails():
    """
    Startet den E-Mail-Abrufprozess.
    Erwartet Konfigurationsdaten für das POP3-Konto.
    """
    request_data = request.json  # Umbenennen, um Konflikte zu vermeiden
    email_receiver = EmailReceiver(request_data)

    try:
        fetched_emails = email_receiver.fetch_emails()
        email_count = len(fetched_emails)
        logger.log("E-Mails erfolgreich abgerufen und an internen Server weitergeleitet.")
        return jsonify({
            "status": "success",
            "message": f"E-Mails erfolgreich abgerufen. Anzahl: {email_count}"
        }), 200
    except Exception as e:
        error_message = f"Fehler beim Abrufen der E-Mails: {e}"
        logger.log(error_message)
        return jsonify({
            "status": "error",
            "message": error_message
        }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.log(f"Unbehandelter Fehler: {e}")
    notify_admin(f"Unbehandelter Fehler: {e}")
    return jsonify({
        "status": "error",
        "message": f"Ein unbehandelter Fehler ist aufgetreten: {e}"
    }), 500

if __name__ == '__main__':
    # Starte den automatischen E-Mail-Abruf in einem separaten Thread
    email_receiver = EmailReceiver(config_data)
    email_thread = threading.Thread(target=email_receiver.receive_emails)
    email_thread.daemon = True
    email_thread.start()

    # Starte das Flask-App-Backend
    app.run(debug=True)
if __name__ == '__main__':

    # Starte den automatischen E-Mail-Abruf in einem separaten Thread
    email_receiver = EmailReceiver(config_data)  # Konfigurationsdaten ggf. anpassen
    email_thread = threading.Thread(target=email_receiver.receive_emails)
    email_thread.daemon = True
    email_thread.start()

    # Starte das Flask-App-Backend
    app.run(debug=True)
