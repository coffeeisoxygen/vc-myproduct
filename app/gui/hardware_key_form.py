import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from app.config.settings import SettingManager
from app.states.state_hardware import HardwareState
from app.utils.encrypt import generate_pc_serial

class HardwareKeyForm(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Konfigurasi Hardware Key")
        self.geometry("400x200")
        self.resizable(False, False)

        # Variabel
        self.serial_var = tk.StringVar()

        # Load config
        self.config_manager = SettingManager(Path("settings.ini"))
        self.hardware_state = HardwareState(self.config_manager)
        self.load_config()

        self.build_form()

    def build_form(self):
        tk.Label(self, text="Hardware Serial Key", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        tk.Label(self, text="Serial key ini digunakan untuk keamanan aplikasi.").pack(pady=(5, 15))
        tk.Entry(self, textvariable=self.serial_var, width=50, state="readonly").pack(padx=10, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Generate New", command=self.revoke_serial).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_serial).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

    def load_config(self):
        stored_id = self.hardware_state.get_stored_id()
        if stored_id:
            self.serial_var.set(stored_id)
        else:
            new_serial = generate_pc_serial().decode()
            self.serial_var.set(new_serial)

    def save_serial(self):
        try:
            self.config_manager.set("Hardwareid", "hardware_id", self.serial_var.get())
            messagebox.showinfo("Sukses", "Hardware ID berhasil disimpan.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan hardware ID: {e}")

    def revoke_serial(self):
        if messagebox.askyesno("Konfirmasi", "Anda yakin ingin generate hardware ID baru?"):
            try:
                new_serial = generate_pc_serial().decode()
                self.serial_var.set(new_serial)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal generate serial baru: {e}")


def show_hardware_key_form(parent=None):
    app = HardwareKeyForm(parent=parent)
    app.grab_set()
    app.wait_window()


# Fungsi dipanggil dari luar, misalnya untuk digunakan di AppState
def safe_show_hardware_form():
    root = tk.Tk()
    root.withdraw()
    show_hardware_key_form(parent=root)
    root.destroy()
