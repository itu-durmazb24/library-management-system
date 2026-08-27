# 📚 Kütüphane Yönetim ve İstatistik Sistemi (CLI)

Bu proje, Python kullanılarak geliştirilmiş, JSON tabanlı veri kalıcılığına (persistence) sahip, nesne yönelimli (OOP) bir Konsol (CLI) Kütüphane Yönetim Sistemidir.

Sistem; kitap ödünç alma/iade süreçlerini, dinamik ceza hesaplamalarını, kullanıcı bazlı durum raporlarını ve kütüphane doluluk oranlarını görselleştirerek sunan dinamik istatistik panellerini yönetir.

---

## 🚀 Öne Çıkan Özellikler

* **Ödünç Alma & İade Mantığı:** Kitapların stok durumunu ve kullanıcı limitlerini kontrol ederek JSON formatında güvenli veri güncellemesi.
* **Kullanıcı Özet Raporu:** Kullanıcının elindeki kitapları, ne kadar süredir elinde tuttuğunu, teslim gününü ve gecikme durumunda günlük ceza tutarını dinamik olarak hesaplama (`datetime` modülü ile).
* **Görsel İstatistik Paneli:** Kütüphanedeki rafta duran, ödünç verilen ve toplam kitap sayılarını ASCII progress bar (ilerleme çubuğu) ile görselleştirme.
* **Hata Toleransı (Error Handling):** `KeyError` ve dosya okuma hatalarına karşı güvenli dictionary erişimleri (`.get()`) ve tip kontrolleri.

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.x
* **Veri Depolama:** JSON (File-based Storage)
* **Dahili Modüller:** `json`, `datetime`

---

## 💻 Kurulum ve Çalıştırma

1. Projeyi klonlayın:
   ```bash
   git clone [https://github.com/itu-durmazb24/library-management-system.git]
