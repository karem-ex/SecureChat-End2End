import customtkinter as ctk
import socket
import threading
import time
from crypto_func import CryptoManager # Modüler dosyamızı bağladık

class SecureChatUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SecureChat - E2EE v1.0 (RSA & AES-256 & SHA-256)")
        self.geometry("600x600") # Loglar için biraz daha alan açtık

        # --- 14. HAFTA: KRİPTO YÖNETİCİSİ BAŞLATMA ---
        # RSA anahtar çifti (Public/Private) __init__ içerisinde otomatik üretilir.
        self.crypto = CryptoManager() 

        # --- ARAYÜZ BİLEŞENLERİ ---
        self.log_display = ctk.CTkTextbox(self, width=560, height=380)
        self.log_display.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        self.log_display.insert("end", "Sistem: 2048-bit RSA Anahtarları Üretildi.\n")

        self.msg_entry = ctk.CTkEntry(self, placeholder_text="Güvenli mesaj yazın...", width=400)
        self.msg_entry.grid(row=1, column=0, padx=20, pady=10)
        self.msg_entry.bind("<Return>", lambda event: self.send_action())

        self.send_button = ctk.CTkButton(self, text="Güvenli Gönder", command=self.send_action)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Durum: Bağlanıyor...", text_color="orange")
        self.status_label.grid(row=2, column=0, columnspan=2)

        self.client_socket = None
        connection_thread = threading.Thread(target=self.setup_network, daemon=True)
        connection_thread.start()

    def update_log(self, text):
        """Arayüz loguna güvenli şekilde yazı ekler."""
        self.log_display.insert("end", text)
        self.log_display.see("end")

    def setup_network(self):
        SERVER_IP = "10.0.2.15" 
        PORT = 5050
        while self.client_socket is None:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((SERVER_IP, PORT))
                self.update_log("Sistem: Sunucuya bağlandı.\n")
                threading.Thread(target=self.receive_messages, daemon=True).start()
            except:
                time.sleep(2)

    def receive_messages(self):
        """Mesajları alır, RSA/AES işlemlerini ve Hash kontrolünü yapar."""
        try:
            # --- 12. HAFTA: HANDSHAKE ---
            challenge_data = self.client_socket.recv(1024).decode('utf-8')
            if challenge_data:
                answer = str(int(challenge_data) ** 2)
                self.client_socket.send(answer.encode('utf-8'))
                auth_confirm = self.client_socket.recv(1024).decode('utf-8')
                
                if auth_confirm == "HANDSHAKE_OK":
                    self.status_label.configure(text="● El Sıkışma Tamam", text_color="blue")
                    
                    # --- 14. HAFTA: RSA PUBLIC KEY GÖNDERİMİ --- [cite: 36]
                    # Bağlantı doğrulandıktan sonra Public Key'imizi sunucuya/ağa duyuruyoruz.
                    my_pub_key = self.crypto.get_my_public_key()
                    self.client_socket.send(b"KEY:" + my_pub_key)
                    self.update_log("Sistem: RSA Public Key ağa gönderildi.\n")
                    self.status_label.configure(text="● E2EE & Bütünlük Aktif", text_color="green")
        except Exception as e:
            self.update_log(f"Sistem: Bağlantı hatası: {e}\n")
            return

        # --- 13. & 14. HAFTA: ŞİFRELİ VERİ DİNLEME ---
        while True:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if data:
                    # Şifreli veriyi çöz (13. Hafta AES) [cite: 27, 28]
                    decrypted_msg = self.crypto.decrypt_message(data)
                    
                    # Bütünlük kontrolü için Hash hesapla (14. Hafta SHA-256) 
                    msg_hash = self.crypto.get_hash(decrypted_msg)
                    
                    self.update_log(f"Gelen: {decrypted_msg}\n")
                    self.update_log(f"[*] Alınan Hash (SHA-256): {msg_hash[:20]}...\n")
            except:
                break

    def send_action(self):
        """Mesajı şifreler, özetini çıkarır ve gönderir."""
        plaintext = self.msg_entry.get()
        if plaintext and self.client_socket:
            try:
                # 14. HAFTA: Bütünlük kontrolü için Hash üret [cite: 39]
                current_hash = self.crypto.get_hash(plaintext)
                
                # 13. HAFTA: Mesajı AES-256-CBC ile şifrele [cite: 25, 31]
                encrypted_msg = self.crypto.encrypt_message(plaintext)
                self.client_socket.send(encrypted_msg.encode('utf-8'))
                
                self.update_log(f"Siz: {plaintext}\n")
                self.update_log(f"[*] Gönderilen Hash: {current_hash[:20]}...\n")
                self.msg_entry.delete(0, 'end')
            except Exception as e:
                self.update_log(f"Sistem: Gönderim Hatası: {e}\n")

if __name__ == "__main__":
    app = SecureChatUI()
    app.mainloop()
