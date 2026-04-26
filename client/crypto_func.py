from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

class CryptoManager:
    def __init__(self, key=None):
        # 13. HAFTA: AES-256 için 32 byte (256 bit) anahtar gereklidir.
        # Eğer anahtar verilmezse test için geçici bir anahtar kullanır.
        self.key = key if key else b'12345678901234567890123456789012'

    def encrypt(self, plaintext):
        """Metni AES-256-CBC ile şifreler ve Base64 formatında döner."""
        try:
            # 21. Madde: CSPRNG ile her mesaj için benzersiz IV üretimi
            iv = os.urandom(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # 29. Madde: UTF-8 ve PKCS7 Padding
            padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            
            # IV ve şifreli veriyi birleştirip iletim için Base64'e çeviriyoruz
            return base64.b64encode(iv + ciphertext).decode('utf-8')
        except Exception as e:
            return f"ENC_ERR: {str(e)}"

    def decrypt(self, encoded_ciphertext):
        """Base64 formatındaki şifreli metni çözer."""
        try:
            raw_data = base64.b64decode(encoded_ciphertext)
            iv = raw_data[:16] # İlk 16 byte IV
            ciphertext = raw_data[16:]
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            return f"[Şifre Çözülemedi]"
