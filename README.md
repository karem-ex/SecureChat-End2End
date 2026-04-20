---

# SecureChat: Uçtan Uca ve Katmanlı Şifreleme (E2EE & Nested Encryption)

SecureChat, modern siber güvenlik protokollerini temel alan, üniversite bitirme projesi kapsamında geliştirilen güvenli bir mesajlaşma platformudur. Proje, sadece mesajın uç noktalar arasında şifrelenmesini (E2EE) değil, aynı zamanda sunucu ile istemci arasındaki taşıma katmanının da ek olarak şifrelenmesini (Nested Encryption) hedefler.

## 11. Hafta: Planlama ve Gereksinim Analizi

Bu hafta, projenin teknoloji yığını belirlenmiş, mimari akış şeması oluşturulmuş ve temel kullanıcı arayüzü (GUI) tasarlanmıştır

### Teknoloji Yığını ve Araç Seçimi
Projenin gereksinim analizi doğrultusunda aşağıdaki teknolojiler seçilmiştir.
* **Programlama Dili:** Python 3.10+ 
* **Kriptografi Kütüphanesi:** `pycryptodome` (AES-256, RSA ve SHA-256 işlemleri için) 
* **Arayüz (GUI):** `CustomTkinter` (Modern ve modüler bir kullanıcı deneyimi için) 
* **Veritabanı:** `SQLite3` (Sunucu tarafında dinamik Identity-Based Discovery ve TTL yönetimi için)
* **Ağ Bağlantısı:** Python `socket` ve `threading` kütüphaneleri

### Mimari Yapı (Nested Encryption)
SecureChat, "Zarf İçinde Zarf" mantığını kullanır:
1.  **İç Katman (E2EE):** Mesaj, alıcının AES anahtarı ile şifrelenir.
2.  **Dış Katman (Transport):** Şifreli paket, sunucunun AES anahtarı ile tekrar şifrelenir.
3.  **Zero-Knowledge:** Sunucu, mesaj içeriğini göremez; sadece dış katmanı açarak mesajı doğru alıcıya yönlendirir.

### Proje Klasör Yapısı
```text
SecureChat/
├── server/             # Sunucu (Kali Linux VM) dosyaları 
├── client/             # İstemci (Client VM ve Host) dosyaları
├── assets/             # Görsel materyaller ve akış şemaları
└── docs/               # Teknik raporlar ve analiz belgeleri 
```

## Laboratuvar Ortamı
Sistem, izole bir **Host-only Adapter** ağı üzerinde üç farklı makinede test edilmektedir:
* **Server:** Kali Linux VM (`192.168.56.10`)
* **Client 1:** Debian/Pardus VM (`192.168.56.11`)
* **Client 2:** Fiziksel Host Makine (`192.168.56.1`)

## Yol Haritası (5 Haftalık Plan)
* **11. Hafta:** Planlama, Analiz ve Arayüz Tasarımı (Tamamlandı)
* **12. Hafta:** Soket Bağlantısı ve Matematiksel Altyapı 
* **13. Hafta:** Simetrik Şifreleme (AES-256) Entegrasyonu
* **14. Hafta:** Asimetrik Şifreleme (RSA) ve Hibrit Yapı 
* **15. Hafta:** Final Sunumu, Rapor ve Canlı Demo

---

### Kurulum ve Çalıştırma
```bash
# Bağımlılıkları yükleyin
pip install pycryptodome customtkinter

# Sunucuyu başlatın (Kali VM)
python server/server_main.py

# İstemciyi başlatın (Client VM/Host)
python client/client_main.py
```

---

### Proje Akış Şeması
```mermaid
sequenceDiagram
    participant C1 as Client-A (Gönderici)
    participant S as Kali Server (VM1)
    participant C2 as Client-B (Alıcı)

    Note over C1: 1. Mesaj Oluşturma (Plaintext)
    Note over C1: 2. E2EE: AES-256 (Client-B Public Key ile)
    C1->>C1: İç Zarf (Encrypted Payload)
    
    Note over C1: 3. Transport: AES-256 (Server Key ile)
    C1->>C1: Dış Zarf (Nested Encryption)
    
    C1->>S: TCP Socket (Port: 5050) - [IP: 192.168.56.10]
    
    Note over S: 4. Sunucu Dış Zarfı Açar (Server Private Key)
    Note over S: 5. SQLite Sorgusu: Nickname -> IP (192.168.56.11)
    S->>C2: Şifreli İç Zarfı Yönlendir (Zero-Knowledge)
    
    Note over C2: 6. Alıcı İç Zarfı Açar (Client-B Private Key)
    Note over C2: 7. Mesaj Çözme (Decryption)
    Note over C2: 8. GUI Görüntüleme (UTF-8)
**Not:** Bu proje, 11-15. haftalar arası haftalık değerlendirme çizelgesindeki kriterlere %100 uyumlu olarak geliştirilmektedir.
