import os
import shutil
import psutil
import ctypes
import subprocess
try:
    import GPUtil
except ImportError:
    GPUtil = None

class RhemeEngine:
    def __init__(self):
        self.junk_categories = {
            "Windows Temp (Sistem Çöpleri)": r'C:\Windows\Temp',
            "Kullanıcı Temp (Uygulama Kalıntıları)": os.environ.get('TEMP'),
            "Prefetch (Eski Çalıştırma Kayıtları)": r'C:\Windows\Prefetch'
        }

    def scan_detailed(self):
        results = {}
        for name, path in self.junk_categories.items():
            total_size = 0
            if path and os.path.exists(path):
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if not os.path.islink(fp):
                            try:
                                total_size += os.path.getsize(fp)
                            except: continue
            results[name] = {"path": path, "size_mb": round(total_size / (1024 * 1024), 2)}
        return results

    def clean_selected(self, selected_paths):
        freed_space = 0
        for path in selected_paths:
            if path and os.path.exists(path):
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    try:
                        size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                            freed_space += size
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except: continue
        return round(freed_space / (1024 * 1024), 2)

    def optimize_system(self):
        try:
            os.system('ipconfig /flushdns')
            return True
        except: return False

    def get_advanced_stats(self):
        stats = {
            "cpu_usage": psutil.cpu_percent(interval=0.1),
            "ram_usage": psutil.virtual_memory().percent,
            "ram_total": round(psutil.virtual_memory().total / (1024**3), 1),
            "battery": "Masaüstü",
            "gpu_usage": "Bulunamadı",
            "gpu_temp": "N/A"
        }
        battery = psutil.sensors_battery()
        if battery:
            plugged = " (Şarjda)" if battery.power_plugged else ""
            stats["battery"] = f"%{battery.percent}{plugged}"
        if GPUtil:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                stats["gpu_usage"] = f"%{round(gpu.load * 100, 1)}"
                stats["gpu_temp"] = f"{gpu.temperature}°C"
        return stats

    # --- YENİ EKLENEN SİLAH DEPOSU ---
    
    def empty_recycle_bin(self):
        """Geri Dönüşüm Kutusunu sessizce boşaltır."""
        try:
            # 7 = Onay sorma, UI gösterme, Ses çıkarma
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            return result == 0
        except: return False

    def open_windows_cleaner(self):
        """Windows'un kendi Disk Temizleme aracını açar."""
        try:
            subprocess.Popen("cleanmgr.exe")
            return True
        except: return False

    def full_network_reset(self):
        """Tüm ağ bağdaştırıcılarını ve Winsock'u sıfırlar."""
        try:
            os.system('ipconfig /release')
            os.system('ipconfig /renew')
            os.system('ipconfig /flushdns')
            os.system('netsh winsock reset')
            return True
        except: return False