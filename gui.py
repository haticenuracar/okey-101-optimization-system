import tkinter as tk
import math

class OkeyArayuz:
    def __init__(self, master, satir_basi_tas=12, 
                 yeniden_baslat_callback=None, 
                 tas_tasi_callback=None, 
                 temizle_callback=None, 
                 manuel_ekle_callback=None,
                 optimize_et_callback=None,
                 tas_sil_callback=None):
        
        self.master = master
        master.title("Okey Optimizasyon")
        
        try:
            master.state('zoomed')
        except:
            master.geometry("1200x800")

        self.is_fullscreen = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

        self.yeniden_baslat_callback = yeniden_baslat_callback
        self.tas_tasi_callback = tas_tasi_callback
        self.temizle_callback = temizle_callback
        self.manuel_ekle_callback = manuel_ekle_callback
        self.optimize_et_callback = optimize_et_callback
        self.tas_sil_callback = tas_sil_callback
        
        self.kutu_genislik = 60
        self.kutu_yukseklik = 85
        self.bosluk = 8
        self.satir_basi_tas = satir_basi_tas 
        
       
        self.son_el_verisi = [None] * 24
        self.son_opt_puan = 0
        self.son_gercek_puan = 0
        self.son_durum_metni = "Hazır"
        self.son_gecerli_indeksler = set()

       
        self.sol_panel = tk.Frame(master, bg="#2E8B57")
        self.sol_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        
        self.frame_ust = tk.Frame(self.sol_panel, bg="#2E8B57")
        self.frame_ust.pack(pady=15, padx=20, fill=tk.X)
        
        btn_style = {"font": ("Segoe UI", 11, "bold"), "bd": 3, "relief": "raised", "height": 2}

        self.btn_restart = tk.Button(self.frame_ust, text="🔄 YENİ DAĞIT", bg="#FF8C00", fg="white", command=self.butona_basildi, **btn_style)
        self.btn_restart.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.btn_trash = tk.Button(self.frame_ust, text="🗑️ TEMİZLE", bg="#DC143C", fg="white", command=self.temizle_basildi, **btn_style)
        self.btn_trash.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.btn_opt = tk.Button(self.frame_ust, text="⚡ OPTİMİZE ET", bg="#1E90FF", fg="white", command=self.optimize_basildi, **btn_style)
        self.btn_opt.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        self.canvas = tk.Canvas(self.sol_panel, bg="#2E8B57", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.drag_data = {"x": 0, "y": 0, "item": None, "index": None}
        self.canvas.bind("<Button-1>", self.on_click)        
        self.canvas.bind("<B1-Motion>", self.on_drag)        
        self.canvas.bind("<ButtonRelease-1>", self.on_release) 
        self.canvas.bind("<Button-3>", self.on_right_click) 

        self.lbl_bilgi = tk.Label(self.sol_panel, text="Hazır | Algoritma: Simulated Annealing", font=("Segoe UI", 14, "bold"), bg="white", relief="sunken", height=2)
        self.lbl_bilgi.pack(side=tk.BOTTOM, fill="x")

        self.sag_panel = tk.Frame(master, width=280, bg="#f5f5f5", relief=tk.RAISED, borderwidth=3)
        self.sag_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(self.sag_panel, text=" Manuel Taş Ekle", bg="#f5f5f5", fg="#333", font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        self.menu_frame = tk.Frame(self.sag_panel, bg="#f5f5f5")
        self.menu_frame.pack(padx=10, pady=5)
        self.menu_olustur()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.master.attributes("-fullscreen", False)
        return "break"

    def on_resize(self, event):
        self.ekrani_ciz(self.son_el_verisi, self.son_opt_puan, self.son_gercek_puan, self.son_durum_metni, 0, self.son_gecerli_indeksler)

    def menu_olustur(self):
        renkler = [0, 1, 2, 3] 
        renk_isimleri = ["Sarı", "Mavi", "Siyah", "Kırmızı"]
        renk_hex = ["#FFD700", "#1E90FF", "#000000", "#FF0000"]

        for i, r_ad in enumerate(renk_isimleri):
            tk.Label(self.menu_frame, text=r_ad[0], font=("Arial", 10, "bold"), fg=renk_hex[i], bg="#f5f5f5").grid(row=0, column=i, pady=5)

        for sayi in range(1, 14):
            for col, renk_kodu in enumerate(renkler):
                btn = tk.Button(
                    self.menu_frame,
                    text=str(sayi),
                    font=("Arial", 10, "bold"),
                    fg=renk_hex[col],
                    bg="white",
                    relief="groove",
                    width=4,
                    command=lambda r=renk_kodu, s=sayi: self.manuel_ekle_basildi(r, s)
                )
                btn.grid(row=sayi, column=col, padx=2, pady=2)
        
        tk.Label(self.sag_panel, text="Özel Taşlar", bg="#f5f5f5", font=("Segoe UI", 12, "bold")).pack(pady=15)
        btn_joker = tk.Button(self.sag_panel, text="★ JOKER EKLE ★", bg="#8A2BE2", fg="white", font=("Segoe UI", 12, "bold"),
                              command=lambda: self.manuel_ekle_basildi("Joker", 0), height=2)
        btn_joker.pack(padx=20, fill=tk.X)

    def butona_basildi(self):
        if self.yeniden_baslat_callback: self.yeniden_baslat_callback()

    def temizle_basildi(self):
        if self.temizle_callback: self.temizle_callback()

    def manuel_ekle_basildi(self, renk, sayi):
        if self.manuel_ekle_callback: self.manuel_ekle_callback(renk, sayi)

    def optimize_basildi(self):
        if self.optimize_et_callback: self.optimize_et_callback()

    def on_right_click(self, event):
        closest = self.canvas.find_closest(event.x, event.y)
        if not closest: return
        item = closest[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("slot_"):
                index = int(tag.split("_")[1])
                if self.tas_sil_callback:
                    self.tas_sil_callback(index)
                break

    def kutu_koordinati_hesapla(self, index):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 100: canvas_w = 1000
        if canvas_h < 100: canvas_h = 600

        toplam_genislik = (self.satir_basi_tas * self.kutu_genislik) + ((self.satir_basi_tas - 1) * self.bosluk)
        start_x = (canvas_w - toplam_genislik) / 2
        toplam_yukseklik = (2 * self.kutu_yukseklik) + (4 * self.bosluk)
        start_y = (canvas_h - toplam_yukseklik) / 2

        satir = index // self.satir_basi_tas
        sutun = index % self.satir_basi_tas
        
        x1 = start_x + sutun * (self.kutu_genislik + self.bosluk)
        y1 = start_y + satir * (self.kutu_yukseklik + (self.bosluk * 6))
        x2 = x1 + self.kutu_genislik
        y2 = y1 + self.kutu_yukseklik
        return x1, y1, x2, y2, (x1+x2)/2, (y1+y2)/2

    def ekrani_ciz(self, el, opt_puan, gercek_puan, durum_metni, sicaklik=0, gecerli_indeksler=None):
        self.son_el_verisi = list(el)
        self.son_opt_puan = opt_puan
        self.son_gercek_puan = gercek_puan
        self.son_durum_metni = durum_metni
        self.son_gecerli_indeksler = gecerli_indeksler

        self.canvas.delete("all") 
        if gecerli_indeksler is None: gecerli_indeksler = set()
        renk_kodlari = {0: "#FFD700", 1: "#1E90FF", 2: "#000000", 3: "#DC143C", "Joker": "purple"}
        
        for satir in range(2):
            start_index = satir * 12
            x1, y1, _, _, _, _ = self.kutu_koordinati_hesapla(start_index)
            _, _, x2, y2, _, _ = self.kutu_koordinati_hesapla(start_index + 11)
            self.canvas.create_rectangle(x1 - 15, y1 - 10, x2 + 15, y2 + 15, fill="#DEB887", outline="#8B4513", width=3)
            self.canvas.create_line(x1 - 15, y2 + 5, x2 + 15, y2 + 5, fill="#8B4513", width=2)

        for i in range(24):
            tas = el[i] if i < len(el) else None
            x1, y1, x2, y2, cx, cy = self.kutu_koordinati_hesapla(i)
            tag_name = f"slot_{i}" 
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#C19A6B", outline="#8B4513", width=1, tags=tag_name)
            
            if tas is not None:
                outline_color = "#00FF00" if i in gecerli_indeksler else "#333"
                outline_width = 3 if i in gecerli_indeksler else 1
                shadow_offset = 3
                self.canvas.create_rectangle(x1+shadow_offset, y1+shadow_offset, x2+shadow_offset, y2+shadow_offset, fill="#333", stipple="gray50", outline="", tags=tag_name)
                
                if tas.sayi == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#E6E6FA", outline="purple", width=3, tags=tag_name)
                    self.canvas.create_text(cx, cy, text="★", fill="red", font=("Arial", 32, "bold"), tags=tag_name)
                    self.canvas.create_text(x1+12, y1+12, text="OKEY", fill="purple", font=("Arial", 7, "bold"), tags=tag_name)
                else:
                    bg_color = "#FFFAF0"
                    if i in gecerli_indeksler: bg_color = "#F0FFF0"
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=outline_color, width=outline_width, tags=tag_name)
                    renk = renk_kodlari.get(tas.renk, "black")
                    self.canvas.create_text(cx, cy, text=str(tas.sayi), fill=renk, font=("Arial", 26, "bold"), tags=tag_name)
                    self.canvas.create_text(x1+10, y1+12, text=str(tas.sayi), fill=renk, font=("Arial", 10, "bold"), tags=tag_name)

        durum_gosterge = "✅ BARAJ GEÇİLDİ!" if gercek_puan >= 101 else "⚠️ BARAJ ALTI"
        bg_color = "#98FB98" if gercek_puan >= 101 else "white"
        fg_color = "#006400" if gercek_puan >= 101 else "red"
        
        bilgi = f" {durum_metni} | PUAN: {gercek_puan} | {durum_gosterge} "
        self.lbl_bilgi.config(text=bilgi, bg=bg_color, fg=fg_color)
        self.master.update()

    def on_click(self, event):
        closest = self.canvas.find_closest(event.x, event.y)
        if not closest: return
        item = closest[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("slot_"):
                index = int(tag.split("_")[1])
                self.drag_data["item"] = item
                self.drag_data["index"] = index
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                self.canvas.tag_raise(tag)
                break

    def on_drag(self, event):
        if self.drag_data["index"] is not None:
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            self.canvas.move(f"slot_{self.drag_data['index']}", delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        source_index = self.drag_data["index"]
        if source_index is not None:
            en_yakin_index = -1
            en_kisa_mesafe = 999999
            for i in range(24): 
                _, _, _, _, cx, cy = self.kutu_koordinati_hesapla(i)
                mesafe = math.sqrt((event.x - cx)**2 + (event.y - cy)**2)
                if mesafe < en_kisa_mesafe:
                    en_kisa_mesafe = mesafe
                    en_yakin_index = i
            if en_yakin_index != -1 and en_kisa_mesafe < 60:
                if self.tas_tasi_callback:
                    self.tas_tasi_callback(source_index, en_yakin_index)
            else:
                self.ekrani_ciz(self.son_el_verisi, self.son_opt_puan, self.son_gercek_puan, self.son_durum_metni, 0, self.son_gecerli_indeksler)
        self.drag_data["index"] = None