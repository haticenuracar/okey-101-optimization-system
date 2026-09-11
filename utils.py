import random
from models import Tas

def deste_olustur():
    tum_taslar = []
    for renk in range(4): 
        for sayi in range(1, 14):
            tum_taslar.append(Tas(renk, sayi))
            tum_taslar.append(Tas(renk, sayi))
    random.shuffle(tum_taslar)
    return tum_taslar

def el_dagit(deste, tas_sayisi=21, toplam_slot=24):
    
    el = deste[:tas_sayisi]
    
    bosluk_sayisi = toplam_slot - tas_sayisi
    for _ in range(bosluk_sayisi):
        el.append(None)
        
    return el