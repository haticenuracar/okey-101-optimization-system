class Tas:
    def __init__(self, renk, sayi):
        self.renk = renk  
        self.sayi = sayi  
        
    def __repr__(self):
        renk_isimleri = ["Sarı", "Mavi", "Siyah", "Kırmızı"]
        return f"[{renk_isimleri[self.renk]} {self.sayi}]"
    
    def __eq__(self, other):
        return self.renk == other.renk and self.sayi == other.sayi

def renk_grup_kontrol(grup):
    """
    Sıralı Kontrol (Örn: Mavi 3-4-5)
    - Jokerler eksiklerin yerini tutar.
    - DUPLICATE (Aynı sayıdan iki tane) varsa YASAKLAR.
    """
    normal_taslar = [t for t in grup if t.sayi != 0]
    joker_sayisi = len(grup) - len(normal_taslar)
    
    if not normal_taslar: return True
    
    renk = normal_taslar[0].renk
    for tas in normal_taslar:
        if tas.renk != renk: return False
    
    sayilar = sorted([t.sayi for t in normal_taslar])
    
    toplam_bosluk = 0
    for i in range(len(sayilar) - 1):
        if sayilar[i] == sayilar[i+1]:
            return False

        fark = sayilar[i+1] - sayilar[i] - 1
        toplam_bosluk += fark
        
    if toplam_bosluk <= joker_sayisi:
        return True
    
    return False

def sayi_grup_kontrol(grup):
    """
    Renkli Grup Kontrol (Örn: Sarı 7, Mavi 7, Siyah 7)
    """
    normal_taslar = [t for t in grup if t.sayi != 0]
    
    if not normal_taslar: return True
    
    sayi = normal_taslar[0].sayi
    renkler = []
    
    for tas in normal_taslar:
        if tas.sayi != sayi: return False
        if tas.renk in renkler: return False 
        renkler.append(tas.renk)
        
    return True