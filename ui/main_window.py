import customtkinter as ctk
from core.engine import RhemeEngine
import threading
import time

class RhemeUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = RhemeEngine()
        self.checkboxes = []
        self.scan_results_data = {}
        self.is_animating = False

        self.title("RhemeCleaner v3.0 - Ultimate Edition")
        self.geometry("1050x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === YAN MENÜ ===
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo = ctk.CTkLabel(self.sidebar, text="RHEME", font=("Orbitron", 32, "bold"), text_color="#ffcc00") # Ufak bir GS sarısı dokunuşu ;)
        self.logo.grid(row=0, column=0, padx=20, pady=(30, 5))
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="v3.0 Ultimate", font=("Segoe UI", 12))
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 30))

        self.btn_clean = ctk.CTkButton(self.sidebar, text="🧹 Sistem Temizliği", anchor="w", height=45, command=lambda: self.show_frame("clean"))
        self.btn_clean.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_boost = ctk.CTkButton(self.sidebar, text="🚀 PC Hızlandırma", anchor="w", height=45, command=lambda: self.show_frame("boost"))
        self.btn_boost.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        self.btn_tools = ctk.CTkButton(self.sidebar, text="🧰 Ekstra Araçlar", anchor="w", height=45, fg_color="#4a4a4a", hover_color="#333333", command=lambda: self.show_frame("tools"))
        self.btn_tools.grid(row=4, column=0, padx=15, pady=5, sticky="ew")

        self.btn_monitor = ctk.CTkButton(self.sidebar, text="📊 Sistem Analizi", anchor="w", height=45, command=lambda: self.show_frame("monitor"))
        self.btn_monitor.grid(row=5, column=0, padx=15, pady=5, sticky="nwe")

        # === ÇERÇEVELER ===
        self.frames = {}
        
        self.frames["clean"] = ctk.CTkFrame(self, fg_color="transparent")
        self.setup_clean_frame()

        self.frames["boost"] = ctk.CTkFrame(self, fg_color="transparent")
        self.setup_boost_frame()

        self.frames["tools"] = ctk.CTkFrame(self, fg_color="transparent")
        self.setup_tools_frame()

        self.frames["monitor"] = ctk.CTkFrame(self, fg_color="transparent")
        self.setup_monitor_frame()

        self.show_frame("clean")
        self.update_monitor()

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

    # --- SİSTEM TEMİZLİĞİ ---
    def setup_clean_frame(self):
        frame = self.frames["clean"]
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Sistem Temizleyici", font=("Segoe UI", 28, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 20))

        self.scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#1a1a1a", corner_radius=15)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

        self.info_lbl = ctk.CTkLabel(self.scroll_frame, text="Tarama başlatılmadı...", text_color="gray", font=("Segoe UI", 16))
        self.info_lbl.pack(pady=40)

        control_frame = ctk.CTkFrame(frame, fg_color="transparent")
        control_frame.grid(row=2, column=0, sticky="ew")

        self.scan_btn = ctk.CTkButton(control_frame, text="TARA", width=180, height=45, font=("Segoe UI", 16, "bold"), command=self.start_scan)
        self.scan_btn.pack(side="left", padx=10)

        self.clean_btn = ctk.CTkButton(control_frame, text="SEÇİLENLERİ TEMİZLE", width=220, height=45, fg_color="#a83232", hover_color="#7a2424", state="disabled", font=("Segoe UI", 16, "bold"), command=self.start_clean)
        self.clean_btn.pack(side="right", padx=10)

    # --- EKSTRA ARAÇLAR SAYFASI (YENİ) ---
    def setup_tools_frame(self):
        frame = self.frames["tools"]
        ctk.CTkLabel(frame, text="Gelişmiş Araç Kutusu", font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(0, 30))

        # Geri Dönüşüm
        ctk.CTkButton(frame, text="🗑️ Geri Dönüşüm Kutusunu Boşalt", width=350, height=50, fg_color="#2b2b2b", hover_color="#1f1f1f", command=self.run_empty_bin).pack(pady=15, anchor="w")
        
        # Windows Disk Temizleyici
        ctk.CTkButton(frame, text="💽 Windows Disk Temizleyicisini Aç", width=350, height=50, fg_color="#2b2b2b", hover_color="#1f1f1f", command=self.engine.open_windows_cleaner).pack(pady=15, anchor="w")
        
        # Ağ Sıfırlama
        ctk.CTkButton(frame, text="🌐 Tam Kapsamlı Ağ Sıfırlama (Admin)", width=350, height=50, fg_color="#8c6b14", hover_color="#634c0e", command=self.run_network_reset).pack(pady=15, anchor="w")
        
        self.tools_status = ctk.CTkLabel(frame, text="", font=("Segoe UI", 14), text_color="green")
        self.tools_status.pack(pady=20, anchor="w")

    # --- HIZLANDIRMA ---
    def setup_boost_frame(self):
        frame = self.frames["boost"]
        ctk.CTkLabel(frame, text="Oyun Modu & Hızlandırma", font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(0, 20))
        ctk.CTkLabel(frame, text="DNS önbelleğini temizler ve ping stabilizasyonu sağlar.", justify="left").pack(anchor="w", pady=(0, 30))

        self.boost_btn = ctk.CTkButton(frame, text="🚀 SİSTEMİ ATEŞLE", width=300, height=60, font=("Segoe UI", 18, "bold"), fg_color="#a82222", hover_color="#7a1818", command=self.boost_system)
        self.boost_btn.pack(pady=20)
        self.boost_status = ctk.CTkLabel(frame, text="", font=("Segoe UI", 14))
        self.boost_status.pack()

    # --- MONİTÖR ---
    def setup_monitor_frame(self):
        frame = self.frames["monitor"]
        ctk.CTkLabel(frame, text="Donanım Radarı", font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(0, 30))

        stats_grid = ctk.CTkFrame(frame, fg_color="#1a1a1a", corner_radius=15)
        stats_grid.pack(fill="both", expand=True, pady=10, padx=10)

        self.lbl_cpu = ctk.CTkLabel(stats_grid, text="CPU:", font=("Consolas", 18))
        self.lbl_cpu.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        self.bar_cpu = ctk.CTkProgressBar(stats_grid, width=400, progress_color="#3498db")
        self.bar_cpu.grid(row=0, column=1, padx=30)

        self.lbl_ram = ctk.CTkLabel(stats_grid, text="RAM:", font=("Consolas", 18))
        self.lbl_ram.grid(row=1, column=0, padx=30, pady=20, sticky="w")
        self.bar_ram = ctk.CTkProgressBar(stats_grid, width=400, progress_color="#e74c3c")
        self.bar_ram.grid(row=1, column=1, padx=30)

        self.lbl_gpu = ctk.CTkLabel(stats_grid, text="GPU: N/A", font=("Consolas", 18))
        self.lbl_gpu.grid(row=2, column=0, padx=30, pady=20, sticky="w")
        
        self.lbl_temp = ctk.CTkLabel(stats_grid, text="Sıcaklık: N/A", font=("Consolas", 18))
        self.lbl_temp.grid(row=3, column=0, padx=30, pady=20, sticky="w")

    # --- ANİMASYON & MANTIK ---
    def pulse_animation(self):
        """Buton yanıp sönme efekti (Animasyon)"""
        if self.is_animating:
            current_color = self.scan_btn.cget("fg_color")
            new_color = "#14375e" if current_color == "#1f538d" else "#1f538d"
            self.scan_btn.configure(fg_color=new_color)
            self.after(500, self.pulse_animation)

    def start_scan(self):
        self.scan_btn.configure(state="disabled", text="ANALİZ EDİLİYOR...")
        self.is_animating = True
        self.pulse_animation() # Animasyonu başlat
        self.info_lbl.pack_forget()
        
        for cb, _ in self.checkboxes:
            cb.destroy()
        self.checkboxes.clear()

        threading.Thread(target=self.scan_thread, daemon=True).start()

    def scan_thread(self):
        time.sleep(1.5) # Tarama süsü
        self.scan_results_data = self.engine.scan_detailed()
        
        self.is_animating = False # Animasyonu durdur
        self.scan_btn.configure(fg_color="#1f538d") # Rengi sabitle
        
        total_junk = 0
        for name, data in self.scan_results_data.items():
            size = data["size_mb"]
            total_junk += size
            cb_text = f"{name}  -  {size} MB"
            cb = ctk.CTkCheckBox(self.scroll_frame, text=cb_text, font=("Segoe UI", 15))
            cb.pack(anchor="w", padx=20, pady=12)
            if size > 0: cb.select()
            self.checkboxes.append((cb, data["path"]))

        self.scan_btn.configure(state="normal", text="YENİDEN TARA")
        if total_junk > 0:
            self.clean_btn.configure(state="normal")
        else:
            self.info_lbl.configure(text="Sistem Tertemiz!", text_color="green")
            self.info_lbl.pack(pady=20)

    def start_clean(self):
        self.clean_btn.configure(state="disabled", text="TEMİZLENİYOR...")
        selected_paths = [path for cb, path in self.checkboxes if cb.get() == 1]
        threading.Thread(target=self.clean_thread, args=(selected_paths,), daemon=True).start()

    def clean_thread(self, paths):
        freed = self.engine.clean_selected(paths)
        time.sleep(1)
        for cb, _ in self.checkboxes:
            cb.destroy()
        self.checkboxes.clear()
        
        self.info_lbl.configure(text=f"🚀 Operasyon Tamamlandı! {freed} MB alan kazanıldı.", text_color="#3a7ebf")
        self.info_lbl.pack(pady=20)
        self.clean_btn.configure(text="SEÇİLENLERİ TEMİZLE")

    def boost_system(self):
        self.boost_btn.configure(state="disabled", text="ATEŞLENİYOR...")
        threading.Thread(target=self.boost_thread, daemon=True).start()

    def boost_thread(self):
        success = self.engine.optimize_system()
        time.sleep(1.5)
        if success:
            self.boost_status.configure(text="Ağ önbelleği temizlendi! Ping düşürüldü.", text_color="#00ff00")
        else:
            self.boost_status.configure(text="Hata oluştu.", text_color="red")
        self.boost_btn.configure(state="normal", text="🚀 SİSTEMİ ATEŞLE")

    def run_empty_bin(self):
        if self.engine.empty_recycle_bin():
            self.tools_status.configure(text="Geri dönüşüm kutusu imha edildi! 🗑️")
        else:
            self.tools_status.configure(text="Kutu zaten boş veya bir hata oluştu.")

    def run_network_reset(self):
        self.tools_status.configure(text="Ağ sıfırlanıyor, internet gidip gelebilir...")
        threading.Thread(target=self.network_thread, daemon=True).start()

    def network_thread(self):
        if self.engine.full_network_reset():
            self.tools_status.configure(text="Ağ bağdaştırıcıları sıfırlandı! PC'yi yeniden başlatmanız tavsiye edilir.")
        else:
            self.tools_status.configure(text="Hata! Bu işlem için programı Yönetici Olarak çalıştırmalısın.", text_color="red")

    def update_monitor(self):
        stats = self.engine.get_advanced_stats()
        self.lbl_cpu.configure(text=f"CPU: %{stats['cpu_usage']}")
        self.bar_cpu.set(stats['cpu_usage'] / 100)
        
        self.lbl_ram.configure(text=f"RAM: %{stats['ram_usage']} ({stats['ram_total']} GB)")
        self.bar_ram.set(stats['ram_usage'] / 100)
        
        self.lbl_gpu.configure(text=f"GPU: {stats['gpu_usage']}")
        self.lbl_temp.configure(text=f"Sıcaklık: {stats['gpu_temp']}")
        
        self.after(1500, self.update_monitor)