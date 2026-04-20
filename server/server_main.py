import socket
import threading
import random
import secrets  # 21. Madde: CSPRNG için gerekli [cite: 21]

# Bağlı olan doğrulanmış istemcileri tutan liste
clients = []

def generate_secure_nonce(length=16):
    """Şifreleme için güvenli rastgele sayı üretir (CSPRNG)[cite: 21]."""
    return secrets.token_bytes(length)

def broadcast(message, sender_socket):
    """Gelen mesajı gönderen hariç tüm bağlı istemcilere iletir."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Bağlantısı kopmuş istemciyi listeden temizle
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket, address):
    print(f"[+] {address} ile fiziksel bağlantı kuruldu. Handshake başlatılıyor...")
    
    try:
        # --- DÖÇ 1: HANDSHAKE (EL SIKIŞMA) PROTOKOLÜ ---
        challenge_num = random.randint(1, 100)
        client_socket.send(str(challenge_num).encode('utf-8'))
        
        # İstemciden cevap bekle (Matematiksel Doğrulama) [cite: 19]
        response = client_socket.recv(1024).decode('utf-8')
        
        if response == str(challenge_num ** 2):
            print(f"[✔] {address} Handshake Başarılı.")
            client_socket.send("HANDSHAKE_OK".encode('utf-8'))
            
            # Doğrulanan istemciyi yayın listesine ekle
            clients.append(client_socket)
            
            # CSPRNG Testi [cite: 21]
            nonce = generate_secure_nonce().hex()
            print(f"[*] Bu oturum için CSPRNG (IV/Nonce): {nonce}")
        else:
            print(f"[✘] {address} Yanlış cevap! Erişim reddedildi.")
            client_socket.close()
            return
        # --- HANDSHAKE SONU ---

        # 12. HAFTA: Şifresiz Mesajlaşma ve İletim (Broadcast) 
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"[*] [{address}] Mesaj İletiliyor: {message}")
            
            # Mesajı diğer istemcilere yay (Broadcast)
            broadcast(data, client_socket)

    except Exception as e:
        print(f"[!] {address} bağlantı hatası: {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"[-] {address} ayrıldı.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Laboratuvar ortamı Kali IP adresi
    server.bind(("192.168.56.10", 5050)) 
    server.listen(5)
    print("[🚀] SecureChat Sunucusu 5050 portunda dinleniyor...")

    while True:
        client_sock, addr = server.accept()
        # Her istemciyi ayrı bir thread'de işle (Modüler yapı) 
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
