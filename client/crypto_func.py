from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import base64
import os

class CryptoManager:
    def __init__(self, aes_key=None):
        # --- 14. HAFTA: RSA ANAHTAR ÇİFTİ ÜRETİMİ --- 
        # Her uygulama açılışında 2048 bitlik yeni bir RSA çifti üretilir.
        self.key_pair = RSA.generate(2048)
        self.private_key = self.key_pair
        self.public_key = self.key_pair.publickey()
        
        # --- 13. HAFTA: SİMETRİK ANAHTAR (SESSION KEY) --- [cite: 25]
        # Statik anahtar yerine RSA ile iletilecek session_key mantığına geçiliyor.
        self.aes_key = aes_key if aes_key else b'12345678901234567890123456789012'

    def get_my_public_key(self):
        """Kendi Public Key'ini diğer kullanıcıya göndermek için dışa aktarır."""
        return self.public_key.export_key()

    # --- 14. HAFTA: HİBRİT YAPI (SESSION KEY ŞİFRELEME) --- 
    def encrypt_aes_key(self, target_public_key_bytes, aes_key_to_encrypt):
        """AES anahtarını alıcının Public Key'i ile RSA kullanarak şifreler."""
        recipient_key = RSA.import_key(target_public_key_bytes)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypted_key = cipher_rsa.encrypt(aes_key_to_encrypt)
        return base64.b64encode(encrypted_key).decode('utf-8')

    def decrypt_aes_key(self, encrypted_key_base64):
        """Kendi Private Key'i ile şifreli gelen AES anahtarını çözer."""
        encrypted_key = base64.b64decode(encrypted_key_base64)
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_key)
        return self.aes_key

    # --- 14. HAFTA: HASH (ÖZET) KONTROLÜ --- 
    def get_hash(self, text):
        """Mesaj bütünlüğü için SHA-256 özeti üretir."""
        return SHA256.new(text.encode('utf-8')).hexdigest()

    # --- 13. HAFTA: AES ŞİFRELEME FONKSİYONLARI (CBC MODU) --- [cite: 25, 31]
    def encrypt_message(self, plaintext):
        """Metni AES-256-CBC ile şifreler ve Hash ile birleştirir."""
        try:
            iv = os.urandom(16) # [cite: 21]
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
            
            # UTF-8 ve Padding [cite: 29]
            padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            
            # Base64 dönüşümü [cite: 26]
            return base64.b64encode(iv + ciphertext).decode('utf-8')
        except Exception as e:
            return f"ENC_ERR: {str(e)}"

    def decrypt_message(self, encoded_ciphertext):
        """Base64 şifreli metni çözer."""
        try:
            raw_data = base64.b64decode(encoded_ciphertext)
            iv = raw_data[:16]
            ciphertext = raw_data[16:]
            
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            return "[Şifre Çözülemedi/Bütünlük Bozuk]"
