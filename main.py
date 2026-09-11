import tkinter as tk
import threading
import time
from utils import deste_olustur, el_dagit
from models import Tas 
from optimizer import benzetim_tavlamasi, durdur, gercek_puan_ve_indeksler, gruplari_duzenle
from gui import OkeyArayuz

mevcut_el = []
app = None
root = None
algoritma_calisiyor = False

def algoritmayi_baslat():
    global mevcut_el, algoritma_calisiyor
    algoritma_calisiyor = True
    
    try:
        en_iyi_genel_el = mevcut_el[:]
        
       
        toplam_tur = 3
        
        for tur in range(1, toplam_tur + 1):
            if not algoritma_calisiyor: break 
            
            print(f"--- TUR {tur} BAŞLIYOR ---")
            
            sonuc_el = benzetim_tavlamasi(
                en_iyi_genel_el, 
                iterasyon=35000,   
                ilk_sicaklik=1500, 
                gui_guncelle=app.ekrani_ciz,
                grafik_ciz=True,
                tur_sayisi=tur
            )
            
            puan_yeni, _ = gercek_puan_ve_indeksler(sonuc_el)
            puan_eski, _ = gercek_puan_ve_indeksler(en_iyi_genel_el)
            
            if puan_yeni >= puan_eski:
                en_iyi_genel_el = sonuc_el
                mevcut_el = sonuc_el 
            
            puan, indeksler = gercek_puan_ve_indeksler(en_iyi_genel_el)
            app.ekrani_ciz(en_iyi_genel_el, 0, puan, f"TUR {tur} TAMAMLANDI", 0, indeksler)
            time.sleep(0.5) 

        puan, indeksler = gercek_puan_ve_indeksler(en_iyi_genel_el)
        app.ekrani_ciz(en_iyi_genel_el, 0, puan, "✅ EN İYİ SONUÇ BULUNDU", 0, indeksler)
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        
    finally:
        algoritma_calisiyor = False

def yeniden_baslat():
    global algoritma_calisiyor, mevcut_el
    if algoritma_calisiyor:
        durdur()
        time.sleep(0.2)
    deste = deste_olustur()
    ham_el = []
    for _ in range(21): ham_el.append(deste.pop())
    
    
    ham_el.sort(key=lambda tas: (tas.renk, tas.sayi))
    
    mevcut_el = [None] * 24
    for i, tas in enumerate(ham_el): mevcut_el[i] = tas
    puan, indeksler = gercek_puan_ve_indeksler(mevcut_el)
    app.ekrani_ciz(mevcut_el, 0, puan, "DAĞITILDI", 0, indeksler)

def optimize_et_butonu():
    global algoritma_calisiyor, mevcut_el
    if not any(t is not None for t in mevcut_el): return
    if algoritma_calisiyor: return
    threading.Thread(target=algoritmayi_baslat, daemon=True).start()

def temizle():
    global mevcut_el, algoritma_calisiyor
    if algoritma_calisiyor:
        durdur()
        algoritma_calisiyor = False
        time.sleep(0.1)
    mevcut_el = [None] * 24
    app.ekrani_ciz(mevcut_el, 0, 0, "TEMİZLENDİ", 0, set())

def tek_tas_sil(index):
    global mevcut_el, algoritma_calisiyor
    if algoritma_calisiyor: return
    mevcut_el[index] = None
    puan, indeksler = gercek_puan_ve_indeksler(mevcut_el)
    app.ekrani_ciz(mevcut_el, 0, puan, "SİLİNDİ", 0, indeksler)

def manuel_ekle(renk, sayi):
    global mevcut_el
    if None not in mevcut_el: return
    yeni_tas = Tas(renk, sayi)
    for i in range(len(mevcut_el) - 1, -1, -1):
        if mevcut_el[i] is None:
            mevcut_el[i] = yeni_tas
            break
            
    mevcut_el = gruplari_duzenle(mevcut_el)
    
    puan, indeksler = gercek_puan_ve_indeksler(mevcut_el)
    app.ekrani_ciz(mevcut_el, 0, puan, "MANUEL EKLEME", 0, indeksler)

def elle_tas_degistir(index1, index2):
    global mevcut_el, algoritma_calisiyor
    if algoritma_calisiyor: return
    mevcut_el[index1], mevcut_el[index2] = mevcut_el[index2], mevcut_el[index1]
    puan, indeksler = gercek_puan_ve_indeksler(mevcut_el)
    app.ekrani_ciz(mevcut_el, 0, puan, "TAŞ TAŞINDI", 0, indeksler)

def main():
    global root, app
    root = tk.Tk()
    app = OkeyArayuz(
        root, 
        satir_basi_tas=12, 
        yeniden_baslat_callback=yeniden_baslat,
        tas_tasi_callback=elle_tas_degistir,
        temizle_callback=temizle,          
        manuel_ekle_callback=manuel_ekle,
        optimize_et_callback=optimize_et_butonu,
        tas_sil_callback=tek_tas_sil
    )
    root.after(100, yeniden_baslat) 
    root.mainloop()

if __name__ == "__main__":
    main()