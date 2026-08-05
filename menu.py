from temel import *
import os


def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')



MENU="""================================================================================
                    📚 KÜTÜPHANE YÖNETİM SİSTEMİ v1.0 📚
================================================================================

  Hoş Geldiniz! 
  Bu sistem, kütüphane envanterini yönetmek, ödünç/iade süreçlerini takip
  etmek ve işlem geçmişini güvenli bir şekilde kayıt altında tutmak için
  tasarlanmıştır.

--------------------------------------------------------------------------------
 🚀  BAŞLATMA VE KURULUM ADIMLARI
--------------------------------------------------------------------------------
  Devam etmek için [ENTER] tuşuna bastığınızda ilk kurulum başlayacaktır.
  Sistem sizden sırasıyla şu parametreleri belirlemenizi isteyecektir:

  1. Maksimum Ödünç Limiti   : Kullanıcı başına verilecek maksimum kitap sayısı.
  2. Maksimum Teslim Süresi  : Ödünç süresi (gün olarak).
  3. Günlük Gecikme Cezası   : Gün başına uygulanacak ceza miktarı.
  4. Yönetici Şifresi        : Hassas işlemlerde kullanılacak güvenlik şifresi.

--------------------------------------------------------------------------------
 💡  KULLANIM İPUÇLARI VE YÖNETİCİ ONAYI
--------------------------------------------------------------------------------
  • Yönetici Yetkileri : Kurulumda belirleyeceğiniz şifre; sistem ayarlarını 
                         değiştirme, geçmiş kayıtları sıfırlama ve kritik 
                         silme işlemlerinde 'Yönetici Onayı' olarak istenecektir.
  • Tarih Formatı      : Sistemdeki tarih girdilerinde 'GG.AA.YYYY' formatını
                         kullanınız. (Boş bırakırsanız bugün otomatik seçilir)
  • Veri Güvenliği     : Tüm değişiklikler anlık olarak JSON dosyalarına
                         güvenli bir şekilde kaydedilmektedir.

================================================================================
       Kurulumu başlatmak ve parametreleri belirlemek için [ENTER]...
================================================================================"""
print(MENU)
input()
ekrani_temizle()
while(True):
    try:
        maksimum_odunc_limiti=int(input("Maksimum ödünç limiti: "))
        break
    except ValueError:
        print("Lütfen sadece sayısal bir değer giriniz!")
while(True):
    try:
        maksimum_teslim_süresi=int(input("Maksimum teslim süresi: "))
        break
    except ValueError:
        print("Lütfen sadece sayısal bir değer giriniz!")
while(True):
    try:
        günlük_gecikme_cezasi=int(input("Günlük gecikme cezası: "))
        break
    except ValueError:
        print("Lütfen sadece sayısal bir değer giriniz!")


print("\nŞİFRE OLUŞTURMA KURALLARI\n" \
"   1. 4 haneli olmalıdır.\n" \
"   2. Sadece rakamlardan oluşmalıdır.\n" \
"   3. Arada boşluk dahil herhangi bir karakter içermemelidir.\n")


while(True):
    sifre=input("Şifre: ")
    if not sifre.isdigit():
        print("Şifre sadece rakamlardan oluşmalıdır. Tekrar deneyiniz.")
        continue
    if not len(sifre)==4:
        print("Şifre 4 haneli olmalıdır. Tekrar deneyiniz.")
        continue
    if sifre.isdigit() and len(sifre)==4:
        print("Şifre başarıyla oluşturulmuştur.")
        break


kutuphane=Kutuphane(sifre)
kutuphane.ayarlar_degistir(maksimum_odunc_limiti,maksimum_teslim_süresi,günlük_gecikme_cezasi)
def cikis_yap():
    kutuphane.log_ekle("PROGRAM KAPATILDI","Tüm veriler kaydedildi. Program kapatılmıştır.")
    print("\n[!]Tüm veriler kaydedildi. Program kapatılıyor... İyi günler!")
    os._exit(0)  


menuyegiris="""
================================================================================
                    Menüye giriş yapmak için [ENTER]...
================================================================================"""
print(menuyegiris)
input()
ekrani_temizle()
GİRİS="""
==========================================================
                KÜTÜPHANE YÖNETİM SİSTEMİ
==========================================================

  [ 1 ] 📚 KİTAP VE ENVANTER YÖNETİMİ
        - Kitap Ekle (Tekli)
        - Kitap Sil
        - Toplu Kitap Sil
        - Kitap Ara
        - ID ile Kitap Getir
        - Kategoriye Göre Listele

  [ 2 ] 🔄 ÖDÜNÇ VE İADE İŞLEMLERİ
        - Ödünç Al
        - Ödünç İade Et / Teslim Al
        - Ödünç Alınabilir Kitaplar
        - Ödünç Verilmiş Kitaplar

  [ 3 ] 📊 LİSTELEME VE İSTATİSTİKLER
        - Tüm kitapları listele  
        - Genel İstatistikler ve Oranlar
        - Kullanıcı Özet Raporu
        - Gecikmiş Ödünç Kitaplar

  [ 4 ] ⚙️ YÖNETİCİ VE SİSTEM AYARLARI
        - Sistem Ayarlarını Değiştir
        - İşlem Geçmişini Sıfırla

----------------------------------------------------------
  [ 0 ] 🚪 Güvenli Çıkış (Yönetici şifresi gerekmektedir)
=========================================================="""
islem1="""
==========================================================
               📚 KİTAP VE ENVANTER YÖNETİMİ
==========================================================
  [ 1 ] Kitap Ekle (Tekli)
  [ 2 ] Kitap Sil
  [ 3 ] Kitap Ara
  [ 4 ] ID ile Kitap Getir
  [ 5 ] Kategoriye Göre Listele

----------------------------------------------------------
  [ 0 ] ↩️ Ana Menüye Dön
==========================================================
"""
islem2="""
==========================================================
               🔄 ÖDÜNÇ VE İADE İŞLEMLERİ
==========================================================
  [ 1 ] Ödünç Al
  [ 2 ] Ödünç İade Et / Teslim Al
  [ 3 ] Ödünç Alınabilir Kitaplar
  [ 4 ] Ödünç Verilmiş Kitaplar

----------------------------------------------------------
  [ 0 ] ↩️ Ana Menüye Dön
==========================================================
"""

islem3="""
==========================================================
               📊 LİSTELEME VE İSTATİSTİKLER
==========================================================
  [ 1 ] Tüm Kitapları Listele
  [ 2 ] Genel İstatistikler ve Oranlar
  [ 3 ] Kullanıcı Özet Raporu
  [ 4 ] Gecikmiş Ödünç Kitaplar

----------------------------------------------------------
  [ 0 ] ↩️ Ana Menüye Dön
==========================================================
"""

islem4="""
==========================================================
               ⚙️ YÖNETİCİ VE SİSTEM AYARLARI
==========================================================
  [ 1 ] Sistem Ayarlarını Değiştir
  [ 2 ] İşlem Geçmişini Sıfırla
  [ 3 ] Şifre Değiştir
  
----------------------------------------------------------
  [ 0 ] ↩️ Ana Menüye Dön
==========================================================
"""



while(True):
    print(GİRİS)
    while(True):
        while(True):
            try:
                islem=int(input("Yapmak istediğiniz işlemi giriniz: "))
                break
            except ValueError:
                print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
        if not 0<=islem<=4:
            print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
        else:
            break
    ekrani_temizle()
    if islem==0:
        while(True):
            alincak_sifre=input("Şifre: ")
            if not alincak_sifre.isdigit():
                print("Şifre sadece rakamlardan oluşmalıdır. Tekrar deneyiniz.")
                continue
            else:
                break
        if alincak_sifre==sifre:
            cikis_yap()
        else:
            print("Şifre yanlış girilmiştir. İşleminiz iptal edilmiştir.")

    if islem==1:
        while(True):
            print(islem1)
            while(True):
                while(True):
                    try:
                        islemmenu=int(input("Yapmak istediğiniz işlemi giriniz: "))
                        break
                    except ValueError:
                        print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                if not 0<=islemmenu<=5:
                    print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                else:
                    break
            if islemmenu==0:
                ekrani_temizle()
                break
            elif islemmenu==1:
                while(True):
                    ekrani_temizle()
                    kitapismi=input("Kitabın ismini giriniz: ")
                    yazar=input("Yazar ismini giriniz: ")
                    id=input("ID giriniz: ")
                    while(True):
                        varmi=kutuphane.id_var_mi(id)
                        if varmi==True:
                            print("Bu id kütüphanede bir kitapta kullanılıyor. Lütfen farklı bir id giriniz: ")
                        else:
                            break
                    kategori=input("Kitabın kategorisini giriniz (Zorunlu değildir): ")
                    if not kategori:
                        kategori=None
                    kitap=Kitap(kitapismi,yazar,id,kategori)
                    veri=kitap.to_dict()
                    kutuphane.kitap_ekle(veri)
                    print("Kitap başarıyla kütüphanemize eklenmiştir\n")
                    dongu=False
                    while(True):
                        devammi=input("Başka bir kitap eklemek ister misiniz? (E/H): ")
                        if devammi.strip().lower()=="H".strip().lower():
                            dongu=True
                            break
                        elif devammi.strip().lower()=="E".strip().lower():
                            break
                        else:
                            print("Yanlış tuşlama yaptınız!")

                    if dongu:
                        break
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==2:
                ekrani_temizle()
                kutuphane.kitap_sil()
                print("Kitap başarıyla kütüphanemizden silinmiştir")
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()
            

            elif islemmenu==3:
                ekrani_temizle()
                print("Bulmak istediğiniz kitabın isminden veya yazar isminden en az birini yazınız")
                name=input("Kitabın ismi (Bilmiyorsanız entera basınız): ")
                if not name:
                    name=None
                writer=input("Yazarın ismi (Bilmiyorsanız entera basınız): ")
                if not writer:
                    writer=None
                kutuphane.kitap_ara(name=name,writer=writer)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==4:
                ekrani_temizle()
                sonuc=kutuphane.id_ile_getir()
                if not sonuc:
                    print("")
                else:
                    print(sonuc)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==5:
                ekrani_temizle()
                kategori=input("Aramak istediğiniz kategoriyi giriniz: ")
                kutuphane.kategoriye_gore_listele(kategori)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

    elif islem==2:
        while(True):
            print(islem2)
            while(True):
                while(True):
                    try:
                        islemmenu=int(input("Yapmak istediğiniz işlemi giriniz: "))
                        break
                    except ValueError:
                        print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                if not 0<=islemmenu<=4:
                    print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                else:
                    break
            if islemmenu==0:
                ekrani_temizle()
                break

            elif islemmenu==1:
                ekrani_temizle()
                id=input("Ödünç alınacak kitabın IDsini giriniz: ")
                kutuphane.odunc_al(id)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==2:
                ekrani_temizle()
                id=input("Ödünç verilecek kitabın IDsini giriniz: ")
                kutuphane.odunc_ver(id)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==3:
                ekrani_temizle()
                print("----------------------------------------------------------\n                Ödünç Alınabilir Kitaplar\n----------------------------------------------------------\n")
                kutuphane.oduncdurumu(False)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()
            elif islemmenu==4:
                ekrani_temizle()
                print("----------------------------------------------------------\n               Ödünç Verilmiş Kitaplar\n----------------------------------------------------------\n")
                kutuphane.oduncdurumu(True)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()
    elif islem==3:
        while(True):
            print(islem3)
            while(True):
                while(True):
                    try:
                        islemmenu=int(input("Yapmak istediğiniz işlemi giriniz: "))
                        break
                    except ValueError:
                        print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                if not 0<=islemmenu<=4:
                    print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                else:
                    break
            if islemmenu==0:
                ekrani_temizle()
                break
            elif islemmenu==1:
                ekrani_temizle()
                print("----------------------------------------------------------\n                       Tüm Kitaplar\n----------------------------------------------------------\n")
                kutuphane.tum_kitaplari_listele()
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==2:
                ekrani_temizle()
                toplam=kutuphane.toplam_kitap_sayisi()
                raf=kutuphane.raftaki_kitap_sayisi()
                oduncsayi=kutuphane.Ödünçteki_kitap_sayisi()
                oran = (oduncsayi / toplam * 100) if toplam > 0 else 0

                dolu_blok = int((oran / 100) * 30)
                bos_blok = 30 - dolu_blok
                bar = "█" * dolu_blok + "░" * bos_blok

                print(f"""
                ================================================================================
                                    📊 KÜTÜPHANE GENEL İSTATİSTİK PANELİ
                ================================================================================

                  📚 Toplam Kitap Sayısı      : {toplam}
                  🟢 Raftaki Kitap Sayısı     : {raf}
                  🔴 Ödünçteki Kitap Sayısı   : {oduncsayi}

                --------------------------------------------------------------------------------
                  📈 ÖDÜNÇLÜK ORANI VE DOLULUK
                --------------------------------------------------------------------------------
                  [{bar}] %{oran:.1f}
  
                ================================================================================
                """)
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()
            elif islemmenu==3:
                ekrani_temizle()
                kutuphane.kullanici_ozet()
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

            elif islemmenu==4:
                ekrani_temizle()
                kutuphane.gecikmisler()
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()

    elif islem==4:
        while(True): 
            while(True):
                alincak_sifre=input("Şifre: ")
                if not alincak_sifre.isdigit():
                    print("Şifre sadece rakamlardan oluşmalıdır. Tekrar deneyiniz.")
                    continue
                else:
                    break
            if alincak_sifre!=sifre:
                print("Girilen şifre yanlıştır. Ana menüye gönderiliyorsunuz...")
                input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                ekrani_temizle()
                break
            else:
                while(True):
                    print(islem4)
                    while(True):
                        while(True):
                            try:
                                islemmenu=int(input("Yapmak istediğiniz işlemi giriniz: "))
                                break
                            except ValueError:
                                print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                        if not 0<=islemmenu<=3:
                            print("Lütfen ekranda gördüğünüz işlemlerin başında gördüğünüz sayıyı giriniz!")
                        else:
                            break
                    ustmenü=False
                    if islemmenu==0:
                        ekrani_temizle()
                        ustmenü=True
                        break

                    elif islemmenu==1:
                        ekrani_temizle()
                        while(True):
                            try:
                                maksimum_odunc_limiti=int(input("Yeni maksimum ödünç limiti: "))
                                break
                            except ValueError:
                                print("Lütfen sadece sayısal bir değer giriniz!")
                        while(True):
                            try:
                                maksimum_teslim_süresi=int(input("Yeni maksimum teslim süresi: "))
                                break
                            except ValueError:
                                print("Lütfen sadece sayısal bir değer giriniz!")
                        while(True):
                            try:
                                günlük_gecikme_cezasi=int(input("Yeni günlük gecikme cezası: "))
                                break
                            except ValueError:
                                print("Lütfen sadece sayısal bir değer giriniz!")

                        kutuphane.ayarlar_degistir(maksimum_odunc_limiti,maksimum_teslim_süresi,günlük_gecikme_cezasi)
                        input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                        ekrani_temizle()
                    

                    elif islemmenu==2:
                        ekrani_temizle()
                        kutuphane.gecmissil()
                        input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                        ekrani_temizle()
                    

                    elif islemmenu==3:
                        ekrani_temizle()
                        while(True):
                            sifre=input("Yeni şifre: ")
                            if not sifre.isdigit():
                                print("Şifre sadece rakamlardan oluşmalıdır. Tekrar deneyiniz.")
                                continue
                            if not len(sifre)==4:
                                print("Şifre 4 haneli olmalıdır. Tekrar deneyiniz.")
                                continue
                            if sifre.isdigit() and len(sifre)==4:
                                print("Şifre başarıyla değiştirilmiştir.")
                                break

                        kutuphane=Kutuphane(sifre)
                        kutuphane.log_ekle("ŞİFRE","Şifre değiştirilmiştir")
                        input("----------------------------------------------------------\n             Devam etmek için Enter'a basınız \n----------------------------------------------------------")
                        ekrani_temizle()
            if ustmenü:
                break