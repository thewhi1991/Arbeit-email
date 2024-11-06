# email_service.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import smtplib
from common.encryption import Encryptor

class EmailService:
    def __init__(self, config):
        self.encryptor = Encryptor()
        with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
            defaults = json.load(f)
        
        self.smtp_server = config.get("smtp_server", defaults["default_smtp_server"])
        self.port = config.get("port", defaults["default_port"])
        # Verschlüsselte Zugangsdaten laden oder verschlüsseln
        self.username = self.encryptor.encrypt(config.get("username", defaults["default_username"]))
        self.password = self.encryptor.encrypt(config.get("password", defaults["default_password"]))
        self.dynamic_ip = config.get("dynamic_ip", defaults["default_dynamic_ip"])
        self.use_pop3 = config.get("use_pop3", defaults["default_use_pop3"])
        self.use_dns = config.get("use_dns", defaults["default_use_dns"])

    def configure_email(self):
        # Entschlüsselung zur Anzeige in der Konfigurationsübersicht
        config_info = {
            "SMTP-Server": self.smtp_server,
            "Port": self.port,
            "Benutzername": self.encryptor.decrypt(self.username),
            "POP3 nutzen": bool(self.use_pop3),
            "DNS konfigurieren": bool(self.use_dns)
        }
        return config_info

    def test_smtp_connection(self):
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                # Entschlüsselte Anmeldeinformationen verwenden
                decrypted_username = self.encryptor.decrypt(self.username)
                decrypted_password = self.encryptor.decrypt(self.password)
                server.login(decrypted_username, decrypted_password)
            return {"status": "success", "message": "SMTP connection successful"}
        except Exception as e:
            return {"status": "error", "message": str(e)}