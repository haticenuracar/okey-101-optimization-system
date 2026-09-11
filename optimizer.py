import random
import math
import time
from models import Tas, renk_grup_kontrol, sayi_grup_kontrol

DURDUR_BAYRAGI = False

def durdur():
    global DURDUR_BAYRAGI
    DURDUR_BAYRAGI = True

def gruplari_duzenle(el):
    
    yeni_el = []
    gecici_grup = []
    
    for tas in el:
        if tas is None:
            if gecici_grup:
                gecici_grup.sort(key=lambda t: t.sayi)
                yeni_el.extend(gecici_grup)
                gecici_grup = []
            yeni_el.append(None)
        else:
            gecici_grup.append(tas)
            
    if gecici_grup:
        gecici_grup.sort(key=lambda t: t.sayi)
        yeni_el.extend(gecici_grup)
        
    return yeni_el

def alt_grup_taramasi(grup, indeks_offset):
    en_iyi_puan = 0
    en_iyi_indeksler = set()
    n = len(grup)
    if n < 3: return 0, set()

    kullanilan_maske = [False] * n 
    i = 0
    while i < n - 2: 
        found = False
        for uzunluk in range(n - i, 2, -1):
            sub_slice = grup[i : i+uzunluk]
            if any(kullanilan_maske[i : i+uzunluk]): continue

            sorted_slice = sorted(sub_slice, key=lambda x: x.sayi)
            
            is_renk = renk_grup_kontrol(sorted_slice)
            is_sayi = False
            if not is_renk: 
                is_sayi = sayi_grup_kontrol(sub_slice)
            
            if is_renk or is_sayi:
                grup_yuz_degeri = 0
                if is_sayi: 
                    ornek = next((t for t in sub_slice if t.sayi != 0), None)
                    val = ornek.sayi if ornek else 0
                    grup_yuz_degeri = val * uzunluk
                elif is_renk: 
                     ilk_gercek = None
                     idx_gercek = -1
                     for k, t in enumerate(sorted_slice):
                         if t.sayi != 0:
                             ilk_gercek = t
                             idx_gercek = k
                             break
                     if ilk_gercek:
                         baslangic = ilk_gercek.sayi - idx_gercek
                         for k in range(uzunluk):
                             grup_yuz_degeri += (baslangic + k)

                puan = (uzunluk * 250) + grup_yuz_degeri
                
                en_iyi_puan += puan
                for k in range(uzunluk):
                    kullanilan_maske[i + k] = True
                    en_iyi_indeksler.add(indeks_offset + i + k)
                i += uzunluk 
                found = True
                break 
        if not found: i += 1 
    return en_iyi_puan, en_iyi_indeksler

def puan_hesapla(el):
    toplam_puan = 0
    gecerli_indeksler = set()
    
    duzenli_el = gruplari_duzenle(el)
    
    gruplar = []
    gecici_grup = []
    gecici_baslangic = 0
    
    for i, tas in enumerate(duzenli_el):
        if tas is None:
            if gecici_grup:
                gruplar.append((gecici_grup, gecici_baslangic))
                gecici_grup = []
            gecici_baslangic = i + 1
        else:
            if not gecici_grup: gecici_baslangic = i
            gecici_grup.append(tas)
    if gecici_grup: gruplar.append((gecici_grup, gecici_baslangic))

    for grup, baslangic_idx in gruplar:
        grup_puani, grup_indeksleri = alt_grup_taramasi(grup, baslangic_idx)
        toplam_puan += grup_puani
        gecerli_indeksler.update(grup_indeksleri)

    return toplam_puan, gecerli_indeksler

def gercek_puan_ve_indeksler(el):
    
    
    saf_puan = 0
    saf_indeksler = set()
    gruplar = []
    gecici_grup = []
    gecici_baslangic = 0
    
    for i, tas in enumerate(el):
        if tas is None:
            if gecici_grup:
                gruplar.append((gecici_grup, gecici_baslangic))
                gecici_grup = []
            gecici_baslangic = i + 1
        else:
            if not gecici_grup: gecici_baslangic = i
            gecici_grup.append(tas)
    if gecici_grup: gruplar.append((gecici_grup, gecici_baslangic))

    for grup, baslangic_idx in gruplar:
        n = len(grup)
        kullanilan_maske = [False] * n
        i = 0
        while i < n - 2:
            found = False
            for uzunluk in range(n - i, 2, -1):
                sub_slice = grup[i : i+uzunluk]
                if any(kullanilan_maske[i : i+uzunluk]): continue
                
                sorted_slice = sorted(sub_slice, key=lambda x: x.sayi)
                is_renk = renk_grup_kontrol(sorted_slice)
                is_sayi = False
                if not is_renk: is_sayi = sayi_grup_kontrol(sub_slice)
                
                if is_renk or is_sayi:
                    grup_toplami = 0
                    if is_sayi: 
                        ornek = next((t for t in sub_slice if t.sayi != 0), None)
                        val = ornek.sayi if ornek else 0 
                        grup_toplami = val * uzunluk
                    elif is_renk: 
                        ilk_gercek = None
                        idx_gercek = -1
                        for k, t in enumerate(sorted_slice):
                            if t.sayi != 0:
                                ilk_gercek = t
                                idx_gercek = k
                                break
                        if ilk_gercek:
                            baslangic_degeri = ilk_gercek.sayi - idx_gercek
                            for k in range(uzunluk):
                                grup_toplami += (baslangic_degeri + k)
                    
                    saf_puan += grup_toplami
                    for k in range(uzunluk):
                        kullanilan_maske[i + k] = True
                        saf_indeksler.add(baslangic_idx + i + k)
                    i += uzunluk
                    found = True
                    break
            if not found: i += 1
    return saf_puan, saf_indeksler

def potansiyel_arkadas_mi(tas1, tas2):
    if tas1 is None or tas2 is None: return False
    if tas1.sayi == tas2.sayi: return tas1.renk != tas2.renk
    if tas1.renk == tas2.renk: return abs(tas1.sayi - tas2.sayi) == 1
    return False

def akilli_komsuluk_uret(el):
    yeni_el = el[:]
    limit = len(el)
    
    if random.random() < 0.70:
        dolu_indeksler = [i for i, t in enumerate(yeni_el) if t is not None]
        if not dolu_indeksler: return yeni_el 
        
        kaynak_idx = random.choice(dolu_indeksler)
        tas = yeni_el[kaynak_idx]
        
        hedef_adaylari = []
        for i, t in enumerate(yeni_el):
            if i == kaynak_idx: continue
            if t is not None and potansiyel_arkadas_mi(tas, t):
                if i + 1 < limit: hedef_adaylari.append(i + 1)
                if i - 1 >= 0: hedef_adaylari.append(i - 1)
                hedef_adaylari.append(i) 

        if hedef_adaylari:
            hedef_idx = random.choice(hedef_adaylari)
            tas = yeni_el.pop(kaynak_idx)
            yeni_el.insert(hedef_idx, tas)
            
            if len(yeni_el) > limit:
                bosluk_silindi = False
                for i in range(len(yeni_el)-1, -1, -1):
                    if yeni_el[i] is None:
                        yeni_el.pop(i)
                        bosluk_silindi = True
                        break
                if not bosluk_silindi: yeni_el.pop() 
            elif len(yeni_el) < limit:
                yeni_el.append(None)
            return yeni_el

    idx_from = random.randint(0, limit-1)
    idx_to = random.randint(0, limit-1)
    if yeni_el[idx_from] is None and yeni_el[idx_to] is None: return yeni_el
    tas = yeni_el.pop(idx_from)
    yeni_el.insert(idx_to, tas)
    return yeni_el

def benzetim_tavlamasi(baslangic_el, iterasyon, ilk_sicaklik, gui_guncelle, grafik_ciz=False, tur_sayisi=1):
    global DURDUR_BAYRAGI
    DURDUR_BAYRAGI = False
    
    mevcut_el = gruplari_duzenle(baslangic_el[:]) 
    mevcut_puan, _ = puan_hesapla(mevcut_el)
    
    en_iyi_el = mevcut_el[:]
    en_iyi_puan = mevcut_puan
    
    sicaklik = ilk_sicaklik
    soguma_orani = 0.9995 
    
    for i in range(iterasyon):
        if DURDUR_BAYRAGI: break
        
        komsusu = akilli_komsuluk_uret(mevcut_el)
        komsusu = gruplari_duzenle(komsusu) 
        
        komsu_puan, _ = puan_hesapla(komsusu)
        
        delta = komsu_puan - mevcut_puan
        
        if delta > 0 or random.random() < math.exp(delta / sicaklik):
            mevcut_el = komsusu
            mevcut_puan = komsu_puan
            
            if mevcut_puan > en_iyi_puan:
                en_iyi_el = mevcut_el[:]
                en_iyi_puan = mevcut_puan
        
        sicaklik *= soguma_orani
        if sicaklik < 1: sicaklik = 1
        
        if i % 200 == 0:
            gosterilecek_el = gruplari_duzenle(mevcut_el)
            gosterim_puani, gosterim_indeksleri = gercek_puan_ve_indeksler(gosterilecek_el)
            durum_mesaji = f"Tur {tur_sayisi} | Analiz... {int((i/iterasyon)*100)}%"
            gui_guncelle(gosterilecek_el, mevcut_puan, gosterim_puani, durum_mesaji, sicaklik, gosterim_indeksleri)

    en_iyi_el = gruplari_duzenle(en_iyi_el)
    return en_iyi_el