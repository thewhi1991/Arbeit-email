# frontend/frontend.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import messagebox
from common.encryption import Encryptor
import requests
import json
from common.logger import setup_logger, log_info, log_error, notify_admin  # Logger importieren

# Lade die Backend-URL aus config.json
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
    config = json.load(f)
backend_url = config["backend_url"]

# Logger initialisieren
setup_logger()

class EmailConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Encryptor-Instanz erstellen
        self.encryptor = Encryptor()
        
        self.title("Email-Konfiguration")
        self.geometry("400x500")

        # Labels und Eingabefelder
        tk.Label(self, text="SMTP-Server:").grid(row=0, column=0, padx=10, pady=10)
        self.smtp_server = tk.Entry(self)
        self.smtp_server.grid(row=0, column=1)

        tk.Label(self, text="SMTP-Port:").grid(row=1, column=0, padx=10, pady=10)
        self.port = tk.Entry(self)
        self.port.grid(row=1, column=1)

        tk.Label(self, text="POP3-Server:").grid(row=2, column=0, padx=10, pady=10)
        self.pop3_server = tk.Entry(self)
        self.pop3_server.grid(row=2, column=1)

        tk.Label(self, text="POP3-Port:").grid(row=3, column=0, padx=10, pady=10)
        self.pop3_port = tk.Entry(self)
        self.pop3_port.grid(row=3, column=1)

        tk.Label(self, text="Benutzername:").grid(row=4, column=0, padx=10, pady=10)
        self.username = tk.Entry(self)
        self.username.grid(row=4, column=1)

        tk.Label(self, text="Passwort:").grid(row=5, column=0, padx=10, pady=10)
        self.password = tk.Entry(self, show='*')
        self.password.grid(row=5, column=1)

        tk.Label(self, text="Intervall in Minuten:").grid(row=6, column=0, padx=10, pady=10)
        self.interval = tk.Entry(self)
        self.interval.grid(row=6, column=1)

        # Buttons
        tk.Button(self, text="Speichern", command=self.save_settings).grid(row=7, column=0, pady=20)
        tk.Button(self, text="E-Mails abrufen", command=self.fetch_emails).grid(row=7, column=1, pady=20)

    def save_settings(self):
        smtp_server = self.smtp_server.get()
        port = self.port.get()
        pop3_server = self.pop3_server.get()
        pop3_port = self.pop3_port.get()
        # Zugangsdaten verschlüsseln
        username = self.encryptor.encrypt(self.username.get())
        password = self.encryptor.encrypt(self.password.get())
        interval = self.interval.get()

        settings = {
            "smtp_server": smtp_server,
            "port": port,
            "pop3_server": pop3_server,
            "pop3_port": pop3_port,
            "username": username.decode(),  # Bytes zu String konvertieren
            "password": password.decode(),
            "interval": interval
        }

        try:
            response = requests.post(f"{backend_url}/configure-email", json=settings)

            if response.status_code == 200:
                messagebox.showinfo("Erfolg", "Einstellungen wurden erfolgreich gespeichert.")
                log_info("Einstellungen erfolgreich gespeichert.")
            else:
                messagebox.showerror("Fehler", f"Fehler beim Speichern: {response.json().get('message')}")
                log_error(f"Fehler beim Speichern der Einstellungen: {response.json().get('message')}")

        except Exception as e:
            messagebox.showerror("Fehler", f"Verbindung zum Backend fehlgeschlagen: {e}")
            log_error(f"Verbindung zum Backend fehlgeschlagen: {e}")
            notify_admin(f"Verbindung zum Backend fehlgeschlagen: {e}")

    def fetch_emails(self):
        # Einstellungen sammeln und verschlüsseln
        smtp_server = self.smtp_server.get()
        port = self.port.get()
        pop3_server = self.pop3_server.get()
        pop3_port = self.pop3_port.get()
        username = self.encryptor.encrypt(self.username.get()).decode()
        password = self.encryptor.encrypt(self.password.get()).decode()
        interval = int(self.interval.get())

        settings = {
            "smtp_server": smtp_server,
            "port": port,
            "pop3_server": pop3_server,
            "pop3_port": pop3_port,
            "username": username,
            "password": password,
            "interval": interval
        }

        try:
            response = requests.post(f"{backend_url}/fetch-emails", json=settings)

            if response.status_code == 200:
                data = response.json()
                messagebox.showinfo("Erfolg", data.get("message", "E-Mails erfolgreich abgerufen."))
                log_info(data.get("message", "E-Mails erfolgreich abgerufen."))
            else:
                data = response.json()
                messagebox.showerror("Fehler", data.get("message", "Fehler beim Abrufen der E-Mails."))
                log_error(f"Fehler beim Abrufen der E-Mails: {data.get('message')}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Verbindung zum Backend fehlgeschlagen: {e}")
            log_error(f"Verbindung zum Backend fehlgeschlagen: {e}")
            notify_admin(f"Verbindung zum Backend fehlgeschlagen: {e}")

# Starten der Anwendung
if __name__ == "__main__":
    app = EmailConfigApp()
    app.mainloop()