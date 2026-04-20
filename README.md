Harika, projenin profesyonel bir vitrine sahip olması için kapsamlı bir `README.md` içeriği hazırladım. Bu dosya, hem projenin teknik derinliğini yansıtacak hem de 11. hafta değerlendirme çizelgesindeki "Gereksinim Analizi ve Araç Seçimi" kriterlerini raporlamış olacaktır.

Aşağıdaki içeriği kopyalayıp GitHub deponuzdaki `README.md` dosyasına yapıştırabilirsiniz:

---

# SecureChat: Uçtan Uca ve Katmanlı Şifreleme (E2EE & Nested Encryption)

SecureChat, modern siber güvenlik protokollerini temel alan, üniversite bitirme projesi kapsamında geliştirilen güvenli bir mesajlaşma platformudur. Proje, sadece mesajın uç noktalar arasında şifrelenmesini (E2EE) değil, aynı zamanda sunucu ile istemci arasındaki taşıma katmanının da ek olarak şifrelenmesini (Nested Encryption) hedefler.

## 11. Hafta: Planlama ve Gereksinim Analizi

Bu hafta, projenin teknoloji yığını belirlenmiş, mimari akış şeması oluşturulmuş ve temel kullanıcı arayüzü (GUI) tasarlanmıştır

### 🛠 Teknoloji Yığını ve Araç Seçimi
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
**Not:** Bu proje, 11-15. haftalar arası haftalık değerlendirme çizelgesindeki kriterlere %100 uyumlu olarak geliştirilmektedir.
