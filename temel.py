import os
import json
from datetime import datetime,timedelta
KLASOR_YOLU = os.path.dirname(os.path.abspath(__file__))
DOSYA_YOLU = os.path.join(KLASOR_YOLU, "kutuphane_verileri.json")
AYARLAR_YOLU = os.path.join(KLASOR_YOLU, "ayarlar.json")
GECMIS_YOLU = os.path.join(KLASOR_YOLU, "gecmis.json")

class Kitap():
    def __init__(self,name,writer,id,kategori=None,odunc_durumu=False,odunc_alma_tarihi=None,kullanici=None):
        self.odunc_alma_tarihi=odunc_alma_tarihi
        self.name=name
        self.writer=writer
        self.id=id
        self.odunc=odunc_durumu
        self.kullanici=kullanici
        self.kategori=kategori

    def to_dict(self):
        bilgiler={
            "Kitap ismi":self.name,
            "Yazar":self.writer,
            "id":self.id,
            "Ödünç Durumu": self.odunc,
            "Kullanici":self.kullanici,
            "Ödünç Alinma Tarihi":self.odunc_alma_tarihi,
            "Kategori":self.kategori
        }
        return bilgiler

class Kutuphane:
    def __init__(self,sifre,dosya_yolu=DOSYA_YOLU):
        self.dosya_yolu = dosya_yolu
        self.kitaplar = []
        self.sifre=sifre

    @property
    def max_odunc_limiti(self):
        with open(AYARLAR_YOLU, "r", encoding="utf-8") as file:
            ayarlar = json.load(file)
        return ayarlar["max_odunc_limiti"]

    @property
    def gunluk_gecikme_cezasi(self):
        with open(AYARLAR_YOLU, "r", encoding="utf-8") as file:
            ayarlar = json.load(file)
        return ayarlar["gunluk_gecikme_cezasi"]

    @property
    def max_teslim_suresi_gun(self):
        with open(AYARLAR_YOLU, "r", encoding="utf-8") as file:
            ayarlar = json.load(file)
        return ayarlar["max_teslim_suresi_gun"]
        
          

    def kitap_ekle(self,bilgiler):
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as file:
                self.kitaplar = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.kitaplar = []
        self.kitaplar.append(bilgiler)
        self.log_ekle("KİTAP EKLENDİ",f"ID: {bilgiler['id']} | '{bilgiler['Kitap ismi']}' kütüphaneye eklendi.")
        with open(self.dosya_yolu,"w",encoding="utf-8") as file:
            json.dump(self.kitaplar, file, ensure_ascii=False, indent=2)

    def kitap_sil(self):
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as file:
                self.kitaplar = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.kitaplar = []
            print("Kütüphanemizde kitap yoktur")
            return
        isHave=False
        while(True):
            bilgiler=input("ID giriniz: ")
            for i in self.kitaplar:
                if i["id"]==bilgiler:
                    isHave=True
            if isHave==False:
                print("Eksik ya da yanlış ID girdiniz.")
            else:
                break
        isim=self.id_ile_getir_new(bilgiler)["Kitap ismi"]
        self.kitaplar=[k for k in self.kitaplar if k["id"]!=bilgiler]
        print("Kitap başarıyla kütüphanemizden silinmiştir")
        self.log_ekle("KİTAP SİLİNDİ",f"ID: {bilgiler} | '{isim}' kütüphaneden silindi.")
        with open(self.dosya_yolu, "w", encoding="utf-8") as file:
            json.dump(self.kitaplar,file,ensure_ascii=False, indent=2)
        if self.kitaplar==[]:
            print("Kütüphanemizdeki son kitap silinmiştir.")
            return
        while(True):
            devammi=input("Başka bir kitap silmek ister misiniz? (E/H): ")
            if devammi.strip().lower()=="H".strip().lower():
                return
            elif devammi.strip().lower()=="E".strip().lower():
                self.kitap_sil()
                return
            else:
                print("Yanlış tuşlama yaptınız!")

    def odunc_al(self,id):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
            isbulundu=False
            for k in self.kitaplar:
                if k["id"]==id:
                    isbulundu=True
                    if k["Ödünç Durumu"] == True:
                        print("Kitap zaten ödünç alınmiş")
                        while(True):
                            devammi=input("Başka bir kitap ödünç almak ister misiniz? (E/H): ")
                            if devammi.strip().lower()=="H".strip().lower():
                                return
                            elif devammi.strip().lower() != "E".strip().lower():
                                print("Yanlış tuşlama yaptınız")
                            else:
                                id=input("Ödünç alınacak kitabın IDsini giriniz: ")
                                self.odunc_al(id)
                                return


                    else:
                        person=input("Kitabi kim alıyor: ")
                        adet=0
                        for i in self.kitaplar:
                            if i.get("Kullanici") == person:
                                adet+=1
                        if adet>=self.max_odunc_limiti:
                            print("Bu kullanıcı, maksimum ödünç limitine ulaşmıştır.")
                            return
                        else:
                            k["Kullanici"]=person
                            k["Ödünç Durumu"] = True
                            bugun_obj = datetime.now()
                            bugun_str = bugun_obj.strftime("%d.%m.%Y")
                            alinma_tarihi_obj=None
                            while(True):
                                ilk_tarih= input("Gün ay yıl (GG.AA.YYYY) şeklinde tarihi giriniz (Herhangi bir şey yazmadan entera basarsanız doğrudan bulunduğunuz zaman kaydedilecektir): ")
                                if not ilk_tarih:
                                    alinma_tarihi_obj=bugun_obj
                                    break
                                try:
                                    alinma_tarihi_obj=datetime.strptime(ilk_tarih, "%d.%m.%Y")
                                    break
                                except ValueError:
                                    print("Hatali tarih formatı! Lütfen GG.AA.YYYY şeklinde ve sadece rakam girin (Örn: 10.07.2026).")

                            k["Ödünç Alinma Tarihi"] = alinma_tarihi_obj.strftime("%d.%m.%Y")
                            son_teslim_obj = alinma_tarihi_obj + timedelta(days=self.max_teslim_suresi_gun)
                            with open(self.dosya_yolu, "w", encoding="utf-8") as file:
                                json.dump(self.kitaplar,file,ensure_ascii=False, indent=2)
                            self.log_ekle("ÖDÜNÇ VERİLDİ",f"{person} -> ID: {id} ('{self.id_ile_getir_new(id)['Kitap ismi']}') kitabını aldı. Son teslim: {son_teslim_obj.strftime('%d.%m.%Y')}")
                            print("Kitap başarıyla ödünç alındı")
                            
                            
                            

                            while(True):
                                devammi=input("Başka bir kitap ödünç almak ister misiniz? (E/H): ")
                                if devammi.strip().lower()=="H".strip().lower():
                                    return
                                elif devammi.strip().lower() != "E".strip().lower():
                                    print("Yanlış tuşlama yaptınız")
                                else:
                                    id=input("Ödünç alınacak kitabın IDsini giriniz: ")
                                    self.odunc_al(id)
                                    return
                        break
            if isbulundu==False:
                print("Kütüphanemizde bu IDye sahip bir kitap bulunmamaktadır")
                while(True):
                    devammi=input("Başka bir kitap ödünç almak ister misiniz? (E/H): ")
                    if devammi.strip().lower()=="H".strip().lower():
                        return
                    elif devammi.strip().lower() != "E".strip().lower():
                        print("Yanlış tuşlama yaptınız")
                    else:
                        id=input("Ödünç alınacak kitabın IDsini giriniz: ")
                        self.odunc_al(id)
                        return
                    
    def odunc_ver(self,id):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
            isbulundu=False
            for k in self.kitaplar:
                if k["id"]==id:
                    isbulundu=True
                    if k["Ödünç Durumu"] == False:
                        print("Kitap zaten geri verilmiş")
                        while(True):
                            devammi=input("Başka bir kitap ödünç verilecek mi? (E/H): ")
                            if devammi.strip().lower()=="H".strip().lower():
                                return
                            elif devammi.strip().lower() != "E".strip().lower():
                                print("Yanlış tuşlama yaptınız")
                            else:
                                id=input("Ödünç verilecek kitabın IDsini giriniz: ")
                                self.odunc_ver(id)
                                return
                    else:
                        bugun_obj = datetime.now()
                        verilme_tarihi=None
                        while(True):
                            sonTarih=input("Gün ay yıl (GG.AA.YYYY) şeklinde tarihi giriniz (Herhangi bir şey yazmadan entera basarsanız doğrudan bulunduğunuz zaman kaydedilecektir): ")
                            if not sonTarih:
                                verilme_tarihi=bugun_obj
                                break
                            try:
                                verilme_tarihi = datetime.strptime(sonTarih, "%d.%m.%Y")
                                break
                            except ValueError:
                                print("Hatalı tarih formatı! Lütfen GG.AA.YYYY şeklinde ve sadece rakam girin (Örn: 10.07.2026).")

                        ilk =datetime.strptime(k["Ödünç Alinma Tarihi"], "%d.%m.%Y")
                        fark = verilme_tarihi - ilk
                        if fark.days>self.max_teslim_suresi_gun:
                            ceza=(fark.days-self.max_teslim_suresi_gun)*self.gunluk_gecikme_cezasi
                            print(f"{k['Kullanici']} adlı kullanıcının teslim süresini {fark.days-self.max_teslim_suresi_gun} gün geciktirmesinden dolayı {ceza} TL para cezası bulunmaktadır.")
                            self.log_ekle("ÖDÜNÇ İADE EDİLDİ",f"{k['Kullanici']} -> ID: {id} {k['Kitap ismi']} kitabını teslim etti. Gecikme: {fark.days-self.max_teslim_suresi_gun} | Ödenen Ceza: {ceza} TL")
                        else:
                            self.log_ekle("ÖDÜNÇ İADE EDİLDİ",f"{k['Kullanici']} -> ID: {id} {k['Kitap ismi']} kitabını teslim etti. Gecikme: 0 | Ödenen Ceza: 0 TL")
                        k["Ödünç Durumu"] = False
                        k["Kullanici"]=None
                        with open(self.dosya_yolu, "w", encoding="utf-8") as file:
                            json.dump(self.kitaplar,file,ensure_ascii=False, indent=2)
                        while(True):
                            devammi=input("Başka bir kitap ödünç verilecek mi? (E/H): ")
                            if devammi.strip().lower()=="H".strip().lower():
                                return
                            elif devammi.strip().lower() != "E".strip().lower():
                                print("Yanlış tuşlama yaptınız")
                            else:
                                id=input("Ödünç verilecek kitabın IDsini giriniz: ")
                                self.odunc_ver(id)
                                return
            if isbulundu==False:
                print("Kütüphanemizde bu IDye sahip bir kitap bulunmamaktadır")
                while(True):
                    devammi=input("Başka bir kitap ödünç verilecek mi? (E/H): ")
                    if devammi.strip().lower()=="H".strip().lower():
                        return
                    elif devammi.strip().lower() != "E".strip().lower():
                        print("Yanlış tuşlama yaptınız")
                    else:
                        id=input("Ödünç verilecek kitabın IDsini giriniz: ")
                        self.odunc_ver(id)
                        return
        
    def kitap_ara(self,name=None,writer=None):
        if name is None and writer is None:
            print("Eksik bilgiler verdiniz.")
            return
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        bulundu=False
        for k in self.kitaplar:
            if name is None and writer is not None:
                if k["Yazar"].strip().lower()==writer.strip().lower():
                    print("Gönderdiğiniz veriler kütüphanemizde bu sonuçlarla eşleşti:\n",k)
                    bulundu=True
            elif name is not None and writer is None:
                if k["Kitap ismi"].strip().lower()==name.strip().lower():
                    print("Gönderdiğiniz veriler kütüphanemizde bu sonuçlarla eşleşti:\n",k)
                    bulundu=True

            elif name is not None and writer is not None:
                if k["Kitap ismi"].strip().lower()==name.strip().lower() and k["Yazar"].strip().lower()==writer.strip().lower():
                    print("Gönderdiğiniz veriler kütüphanemizde bu sonuçla eşleşti:\n",k)
                    bulundu=True
        if not bulundu:
            print("Gönderdiğiniz verilerle eşleşen bir kitap bulunamadı.")
    def id_ile_getir(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        bulundu=False
        while(True):
            id=input("Aramak istediğiniz kitabın idsini giriniz: ")
            for k in self.kitaplar:
                if k["id"]==id:
                    bulundu=True
                    return k
            if bulundu==False:
                print("Eksik ya da hatalı tuşlama yaptınız")
                while(True):
                    devammi=input("Devam etmek ister misiniz? (E/H): ")
                    if devammi.strip().lower()=="H".strip().lower():
                        return
                    elif devammi.strip().lower()=="H".strip().lower():
                        break
                    else:
                        print("Yanlış tuşlama yaptınız. Tekrar deneyiniz.")

    def tum_kitaplari_listele(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        for k in self.kitaplar:
            print(k)

    def oduncdurumu(self,odunc_mu):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        
        if odunc_mu==True:
            print("\n----------------------------------------------------------\n                  Ödünç Verilmiş Kitaplar\n----------------------------------------------------------\n")
            for k in self.kitaplar:
                if k["Ödünç Durumu"] == True:
                    print(k)
        
        elif odunc_mu==False:
            print("\n----------------------------------------------------------\n                Kitaplıkta Bulunan Kitaplar\n----------------------------------------------------------\n")
            for k in self.kitaplar:
                if k["Ödünç Durumu"] == False:
                    print(k)

    def toplam_kitap_sayisi(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        adet=0
        for k in self.kitaplar:
            adet+=1
        return adet

    def raftaki_kitap_sayisi(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
            adet=0
            for k in self.kitaplar:
                if k["Ödünç Durumu"]==False:
                    adet+=1
            return adet

    def Ödünçteki_kitap_sayisi(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
            adet=0
            for k in self.kitaplar:
                if k["Ödünç Durumu"]==True:
                    adet+=1
            return adet


    def kullanici_ozet(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        adet=0
        name=input("Hangi kullanıcının özetini çıkarmak istiyosunuz: ")
        for i in self.kitaplar:
            if(i.get("Kullanici") and i["Kullanici"].strip().lower()==name.strip().lower()):
                adet+=1

        if(adet==0):
            print("Bu kullanıcı kütüphanemizden kitap ödünç almamıştır")
            return

        print(f"=== KULLANICI ÖZETİ: {name} ===\nToplam Ödünç Alınan Kitap: {adet} / Limit: {self.max_odunc_limiti}\n\n")
        sayi=0
        for i in self.kitaplar:
            if(i.get("Kullanici") and i["Kullanici"].strip().lower()==name.strip().lower()):
                sayi+=1
                bugun = datetime.now()
                ilk =datetime.strptime(i["Ödünç Alinma Tarihi"], "%d.%m.%Y")
                fark = bugun - ilk
                if fark.days<self.max_teslim_suresi_gun:
                    kalan=self.max_teslim_suresi_gun-fark.days
                    print(f"{sayi}. {i['Kitap ismi']} - {i['Yazar']} (ID: {i['id']})\n  - Alınma Tarihi: {i['Ödünç Alinma Tarihi']}\n  - Durum: {fark.days} gündür elinde (Kalan Süre: {kalan} gün)")
                elif fark.days==self.max_teslim_suresi_gun:
                    print(f"{sayi}. {i['Kitap ismi']} - {i['Yazar']} (ID: {i['id']})\n  - Alınma Tarihi: {i['Ödünç Alinma Tarihi']}\n  - Durum: {fark.days} gündür elinde (Bugün teslim edilmesi gerekiyor)")
                else:
                    kalan=fark.days-self.max_teslim_suresi_gun
                    print(f"{sayi}. {i['Kitap ismi']} - {i['Yazar']} (ID: {i['id']})\n  - Alınma Tarihi: {i['Ödünç Alinma Tarihi']}\n  - Durum: {fark.days} gündür elinde ({kalan} Gün Gecikme - Güncel Ceza: {kalan*self.gunluk_gecikme_cezasi} TL)")

    def gecikmisler(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        adet=0
        sayi=0
        bugun = datetime.now()
        bugun_str = bugun.strftime("%d.%m.%Y")
        for i in self.kitaplar:
            if i["Ödünç Durumu"]==True:
                ilk =datetime.strptime(i["Ödünç Alinma Tarihi"], "%d.%m.%Y")
                fark = bugun - ilk
                if(fark.days>self.max_teslim_suresi_gun):
                    adet+=1
        
        print("==================================================\n       ⚠️  GECİKMİŞ KİTAPLAR VE CEZA RAPORU\n==================================================\n")
        if adet==0:
            print(f"Rapor Tarihi: {bugun_str}\n\n✅ Harika! Şu an teslim süresi geçmiş veya gecikmeye düşmüş kitap bulunmuyor.")
        else:
            print(f"Rapor Tarihi: {bugun_str} | Sınır: {self.max_teslim_suresi_gun} | Günlük Ceza: {self.gunluk_gecikme_cezasi}\n\n")
            toplam=0
            for i in self.kitaplar:
                if i["Ödünç Durumu"]==True:
                    ilk =datetime.strptime(i["Ödünç Alinma Tarihi"], "%d.%m.%Y")
                    fark = bugun - ilk
                    if(fark.days>self.max_teslim_suresi_gun):
                        sayi+=1
                        ceza=(fark.days-self.max_teslim_suresi_gun)*self.gunluk_gecikme_cezasi
                        print(f"{sayi}. {i['Kitap ismi']} (ID: {i['id']})\n")
                        print(f"    • Kullanıcı      : {i['Kullanici']}")
                        print(f"    • Alınma Tarihi  : {i['Ödünç Alinma Tarihi']}")
                        print(f"    • Geçen Süre     : {fark.days} gün ({fark.days-self.max_teslim_suresi_gun} gün gecikti)")
                        print(f"    • Güncel Ceza    : {ceza} TL")
                        toplam+=ceza

            print("--------------------------------------------------\n")
            print(f"TOPLAM GECİKEN KİTAP : {sayi}\n")
            print(f"TOPLAM BİRİKEN CEZA  : {toplam} TL")
            print("==================================================")

    def ayarlar_degistir(self,yeni_limit,yeni_sure,yeni_ceza):
        with open(AYARLAR_YOLU, "r", encoding="utf-8") as file:
            yeni_ayarlar = json.load(file)
        yeni_ayarlar = {
            "max_teslim_suresi_gun": yeni_sure,
            "gunluk_gecikme_cezasi": yeni_ceza,
            "max_odunc_limiti": yeni_limit
            }
        with open(AYARLAR_YOLU, "w", encoding="utf-8") as file:
            json.dump(yeni_ayarlar, file, indent=2, ensure_ascii=False)
        print("Ayarlar başarıyla güncellendi!")
        

        

    def log_ekle(self, islem_tipi, detay):
        try:
            with open(GECMIS_YOLU, "r", encoding="utf-8") as file:
                gecmis = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            gecmis = []  
        yeni_kayit = {
            "tarih": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "islem": islem_tipi,
            "detay": detay
        }
        gecmis.append(yeni_kayit)
        with open(GECMIS_YOLU, "w", encoding="utf-8") as file:
            json.dump(gecmis, file, indent=2, ensure_ascii=False)

    def kategoriye_gore_listele(self,kategori):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
            isHave=False
        for i in self.kitaplar:
            if i.get("Kategori") and i["Kategori"].strip().lower()==kategori.strip().lower():
                if i["Ödünç Durumu"]==True:
                    print(f"{i['id']} -> {i['Kitap ismi'] } -> {i['Yazar']} (Bu kitap ödünç alınmış)")
                else:
                    print(f"{i['id']} -> {i['Kitap ismi'] } -> {i['Yazar']} (Bu kitap kütüphanemizde mevcut)")
                isHave=True
        if isHave==False:
            print("Bu kategoriyle eşleşen kitabımız bulunmamaktadır")


    def gecmissil(self):
        try:
            with open(GECMIS_YOLU, "r", encoding="utf-8") as file:
                gecmis = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            gecmis = []

        
        while(True):
            eminmi=input("İşlemleri onaylıyor musunuz? (E/H): ")
            if eminmi.strip().lower()=="H".strip().lower():
                print("Geçmiş silme işlemi iptal edilmiştir")
                return
            elif eminmi.strip().lower() != "E".strip().lower():
                print("Yanlış tuşlama yaptınız")
            else:
                gecmis=[]
                with open(GECMIS_YOLU, "w", encoding="utf-8") as file:
                    json.dump(gecmis, file, indent=2, ensure_ascii=False)
                print("Geçmiş silinmiştir")
                return

    def toplukitapekle(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)
        while(True):
            name=input("Kitap ismini giriniz: ")
            yazar=input("Yazar ismini giriniz: ")
            print("ID giriniz (Bir id birden fazla kitapta aynı anda olamaz): ")
            while(True):
                id=input()
                isHave=False
                for i in self.kitaplar:
                    if i["id"]==id:
                        isHave=True
                        break
                if isHave==True:
                    print("Bu id kütüphanede bir kitapta kullanılıyor. Lütfen farklı bir id giriniz: ")
                else:
                    break
            kategori=input("Kategori giriniz (Zorunlu değildir): ")
            if not kategori:
                kategori=None
            kitap=Kitap(name,yazar,id,kategori)
            veri=kitap.to_dict()
            self.kitap_ekle(veri)
            print("Kitap başarıyla kütüphanemize eklenmiştir\n")
            while(True):
                devammi=input("Başka kitap eklemek istiyor musunuz? (E/H): ")
                if devammi.strip().lower()=="H".strip().lower():
                    return
                elif devammi.strip().lower() != "E".strip().lower():
                    print("Yanlış tuşlama yaptınız")
                else:
                    break

    def id_var_mi(self,id):
        with open(self.dosya_yolu, "r", encoding="utf-8") as file:
            self.kitaplar = json.load(file)

        for i in self.kitaplar:
            isHave=False
            for i in self.kitaplar:
                if i["id"]==id:
                    isHave=True
                    break

            return isHave

    def toplukitapsil(self):
        while(True):
            self.kitap_sil()
            with open(self.dosya_yolu, "r", encoding="utf-8") as file:
                self.kitaplar = json.load(file)
            if self.kitaplar==[]:
                break
            while(True):
                devammi=input("Başka kitap silmek istiyor musunuz? (E/H): ")
                if devammi.strip().lower()=="H".strip().lower():
                    return
                elif devammi.strip().lower() != "E".strip().lower():
                    print("Yanlış tuşlama yaptınız")
                else:
                    break
    def id_ile_getir_new(self,id):
            with open(self.dosya_yolu, "r", encoding="utf-8") as file:
                self.kitaplar = json.load(file)

            for k in self.kitaplar:
                if k["id"]==id:
                    return k
