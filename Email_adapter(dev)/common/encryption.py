# filepath: /c:/Users/josha/Documents/arbeit/Email_adapter(dev)/common/encryption.py
from cryptography.fernet import Fernet
import os

class Encryptor:
    def __init__(self, key_file='secret.key'):
        self.key_file = os.path.join(os.path.dirname(__file__), key_file)
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)

    def load_or_create_key(self):
        # Prüfen, ob der Schlüssel bereits existiert
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
        else:
            # Generiere einen neuen Schlüssel und speichere ihn
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        return key

    def encrypt(self, data):
        # Verschlüsseln der Daten
        return self.cipher.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        # Entschlüsseln der Daten
        return self.cipher.decrypt(encrypted_data).decode()
