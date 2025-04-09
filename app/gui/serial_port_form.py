import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from app.config.settings import SettingManager

class SerialPortForm(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Konfigurasi Serial Port")
        self.geometry("400x250")
        self.resizable(False, False)

        # Variabel
        self.ip_var = tk.StringVar()
        self.port_var = tk.StringVar()

        # Load config
        self.config_manager = SettingManager(Path("settings.ini"))
        self.load_config()

        self.build_form()

    def build_form(self):
        # Form layout
        tk.Label(self, text="IP Address").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.ip_var).pack(fill="x", padx=10)

        tk.Label(self, text="Port").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.port_var).pack(fill="x", padx=10)

        # Tombol
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Test", command=self.test_ip_port).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_ip_port).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

    def load_config(self):
        self.ip_var.set(self.config_manager.get("APP", "ip", "127.0.0.1") or "127.0.0.1")
        self.port_var.set(self.config_manager.get("APP", "port", "8000") or "8000")

    def test_ip_port(self):
        messagebox.showinfo("Test", f"Tes koneksi ke {self.ip_var.get()}:{self.port_var.get()}")

    def save_ip_port(self):
        try:
            self.config_manager.set("APP", "ip", self.ip_var.get())
            self.config_manager.set("APP", "port", self.port_var.get())
            messagebox.showinfo("Sukses", "IP dan Port berhasil disimpan")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")


def show_serial_port_form(parent=None):
    app = SerialPortForm(parent=parent)
    app.grab_set()
    app.wait_window()

def safe_show_serial_port_form():
    root = tk.Tk()
    root.withdraw()
    show_serial_port_form(parent=root)
    root.destroy()
