# filepath: /c:/Users/josha/Documents/arbeit/Email_adapter(dev)/backend/email_receiver.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import poplib
import email
from common.encryption import Encryptor
from common.logger import Logger
import smtplib
import time
import threading

class EmailReceiver:
    def __init__(self, config):
        self.encryptor = Encryptor()
        self.pop3_server = config["pop3_server"]
        self.port = config["pop3_port"]
        # Zugangsdaten entschlüsseln
        self.username = self.encryptor.decrypt(config["username"])
        self.password = self.encryptor.decrypt(config["password"])
        self.interval = config.get("interval", 5)
        self.logger = Logger()
        self.internal_smtp_server = config.get("internal_smtp_server", "localhost")
        self.internal_smtp_port = config.get("internal_smtp_port", 25)

    def fetch_emails(self):
        max_attempts = 5  # Maximale Anzahl der Versuche
        attempt = 0  # Zähler für Versuche

        while attempt < max_attempts:
            try:
                server = poplib.POP3_SSL(self.pop3_server, self.port)
                try:
                    server.user(self.username)
                    server.pass_(self.password)

                    # Holen der Anzahl der E-Mails
                    num_messages = len(server.list()[1])
                    fetched_emails = []

                    # Alle E-Mails abrufen
                    for i in range(num_messages):
                        raw_email = b"\n".join(server.retr(i + 1)[1])
                        msg = email.message_from_bytes(raw_email)
                        fetched_emails.append(msg)
                        self.logger.log(f"E-Mail empfangen: {msg['subject']} von {msg['from']}")

                        # E-Mail weiterleiten
                        self.forward_email(msg)

                    return fetched_emails
                finally:
                    server.quit()

            except Exception as e:
                attempt += 1  # Versuchszähler erhöhen
                self.logger.log(f"Fehler beim Abrufen von E-Mails: {e}. Versuch {attempt} von {max_attempts}.")
                if attempt >= max_attempts:
                    self.logger.log(f"Maximale Anzahl der Versuche erreicht. E-Mails konnten nicht abgerufen werden.")
                    return []  # Optional: geben Sie einen speziellen Wert oder eine Ausnahme zurück
                time.sleep(5)  # Wartezeit zwischen den Versuchen, z.B. 5 Sekunden

    def forward_email(self, msg):
        try:
            with smtplib.SMTP(self.internal_smtp_server, self.internal_smtp_port) as server:
                server.send_message(msg)
                self.logger.log(f"E-Mail weitergeleitet an internen Server: {msg['subject']}")
        except Exception as e:
            self.logger.log(f"Fehler bei der Weiterleitung der E-Mail: {e}")

    def receive_emails(self):
        # Endlosschleife für wiederholtes Abrufen der E-Mails im Intervall
        while True:
            self.fetch_emails()
            time.sleep(self.interval * 60)  # Wartezeit entsprechend dem Intervall in Minuten