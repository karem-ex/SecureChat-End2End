import customtkinter as ctk
import socket
import threading
import time

class SecureChatUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SecureChat - E2EE v1.0")
        self.geometry("600x550")

        # --- ARAYÜZ BİLEŞENLERİ ---
        self.log_display = ctk.CTkTextbox(self, width=560, height=350)
        self.log_display.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        self.log_display.insert("end", "Sistem: Başlatılıyor...\n")

        self.msg_entry = ctk.CTkEntry(self, placeholder_text="Mesajınızı yazın...", width=400)
        self.msg_entry.grid(row=1, column=0, padx=20, pady=10)
        # Enter tuşuna basıldığında da mesaj gönderilmesi için bind
        self.msg_entry.bind("<Return>", lambda event: self.send_action())

        self.send_button = ctk.CTkButton(self, text="Gönder", command=self.send_action)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Durum: Bağlanıyor...", text_color="orange")
        self.status_label.grid(row=2, column=0, columnspan=2)

        self.client_socket = None
        # Bağlantıyı arayüzü dondurmamak için ayrı thread'de başlat
        connection_thread = threading.Thread(target=self.setup_network, daemon=True)
        connection_thread.start()

    def setup_network(self):
        """Socket bağlantısını kurar."""
        # Host-only Adapter ağındaki Kali Server IP
        SERVER_IP = "192.168.56.10" 
        PORT = 5050
        
        while self.client_socket is None:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((SERVER_IP, PORT))
                
                self.update_log("Sistem: Sunucuya bağlandı. Handshake yapılıyor...\n")
                self.status_label.configure(text="● El Sıkışma Yapılıyor", text_color="blue")
                
                # Mesaj dinleme ve Handshake sürecini başlat
                threading.Thread(target=self.receive_messages, daemon=True).start()
            except Exception as e:
                self.status_label.configure(text=f"● Sunucu Bekleniyor...", text_color="orange")
                time.sleep(2)

    def update_log(self, text):
        """Arayüz loguna güvenli şekilde yazı ekler."""
        self.log_display.insert("end", text)
        self.log_display.see("end")

    def receive_messages(self):
        """Handshake ve sonrasındaki mesaj trafiğini yönetir."""
        try:
            # --- 12. HAFTA: DÖÇ 1 - HANDSHAKE --- 
            # 1. Challenge sayısını al
            challenge_data = self.client_socket.recv(1024).decode('utf-8')
            if challenge_data:
                challenge_num = int(challenge_data)
                # 2. Matematiksel yanıtı gönder (Karesi) [cite: 19]
                answer = str(challenge_num ** 2)
                self.client_socket.send(answer.encode('utf-8'))
                
                # 3. Onay bekle
                auth_confirm = self.client_socket.recv(1024).decode('utf-8')
                if auth_confirm == "HANDSHAKE_OK":
                    self.status_label.configure(text="● Sunucu Çevrimiçi (Güvenli)", text_color="green")
                    self.update_log("Sistem: Handshake Başarılı. İletişim aktif.\n")
                else:
                    self.update_log("Sistem: Handshake reddedildi.\n")
                    self.client_socket.close()
                    return
        except Exception as e:
            self.update_log(f"Sistem: Bağlantı Hatası: {e}\n")
            return

        # --- 12. HAFTA: ŞİFRESİZ MESAJLAŞMA DÖNGÜSÜ --- 
        while True:
            try:
                msg_bytes = self.client_socket.recv(1024)
                if not msg_bytes:
                    break
                msg = msg_bytes.decode('utf-8')
                self.update_log(f"Gelen: {msg}\n")
            except:
                self.status_label.configure(text="● Bağlantı Koptu", text_color="red")
                break

    def send_action(self):
        """Mesajı sunucuya gönderir."""
        msg = self.msg_entry.get()
        if msg and self.client_socket:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                self.update_log(f"Siz: {msg}\n")
                self.msg_entry.delete(0, 'end')
            except:
                self.update_log("Sistem: Mesaj gönderilemedi!\n")

if __name__ == "__main__":
    app = SecureChatUI()
    app.mainloop()
