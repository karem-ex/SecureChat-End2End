import customtkinter as ctk
import socket
import threading
import time
from crypto_func import CryptoManager # Modüler dosyamızı bağladık

class SecureChatUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SecureChat - E2EE v1.0 (AES-256 Aktif)")
        self.geometry("600x550")

        # 13. HAFTA: Şifreleme yöneticisini başlatıyoruz
        # ÖNEMLİ: Anahtar tam 32 karakter olmalıdır.
        self.crypto = CryptoManager(b"mysecretpassword32charpassword!!") 

        # --- ARAYÜZ BİLEŞENLERİ ---
        self.log_display = ctk.CTkTextbox(self, width=560, height=350)
        self.log_display.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        self.log_display.insert("end", "Sistem: Kripto Modülleri Yüklendi.\n")

        self.msg_entry = ctk.CTkEntry(self, placeholder_text="Şifreli mesajınızı yazın...", width=400)
        self.msg_entry.grid(row=1, column=0, padx=20, pady=10)
        self.msg_entry.bind("<Return>", lambda event: self.send_action())

        self.send_button = ctk.CTkButton(self, text="Şifreli Gönder", command=self.send_action)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Durum: Bağlanıyor...", text_color="orange")
        self.status_label.grid(row=2, column=0, columnspan=2)

        self.client_socket = None
        connection_thread = threading.Thread(target=self.setup_network, daemon=True)
        connection_thread.start()

    def update_log(self, text):
        self.log_display.insert("end", text)
        self.log_display.see("end")

    def setup_network(self):
        SERVER_IP = "192.168.56.10" 
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
        """Mesajları alır ve şifresini çözer."""
        try:
            # --- 12. HAFTA: HANDSHAKE ---
            challenge_data = self.client_socket.recv(1024).decode('utf-8')
            if challenge_data:
                answer = str(int(challenge_data) ** 2)
                self.client_socket.send(answer.encode('utf-8'))
                auth_confirm = self.client_socket.recv(1024).decode('utf-8')
                if auth_confirm == "HANDSHAKE_OK":
                    self.status_label.configure(text="● Uçtan Uca Şifreleme Aktif", text_color="green")
                    self.update_log("Sistem: Güvenli kanal doğrulandı.\n")
        except: return

        # --- 13. HAFTA: ŞİFRELİ VERİ DİNLEME ---
        while True:
            try:
                # Sunucudan şifreli Base64 verisi gelecek
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    # Şifreyi modüler dosyamızla çözüyoruz
                    decrypted_msg = self.crypto.decrypt(data)
                    self.update_log(f"Gelen (Şifreli): {data[:15]}...\n")
                    self.update_log(f"Gelen: {decrypted_msg}\n")
            except:
                break

    def send_action(self):
        """Mesajı şifreler ve gönderir."""
        plaintext = self.msg_entry.get()
        if plaintext and self.client_socket:
            try:
                # 13. HAFTA: Şifreleme fonksiyonunu çağırıyoruz
                encrypted_msg = self.crypto.encrypt(plaintext)
                self.client_socket.send(encrypted_msg.encode('utf-8'))
                
                self.update_log(f"Siz: {plaintext}\n")
                self.msg_entry.delete(0, 'end')
            except Exception as e:
                self.update_log(f"Sistem: Şifreleme Hatası: {e}\n")

if __name__ == "__main__":
    app = SecureChatUI()
    app.mainloop()
