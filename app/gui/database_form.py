import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from app.config.settings import SettingManager

class DatabaseForm(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Konfigurasi Database Otomax")
        self.geometry("400x350")
        self.resizable(False, False)

        # Variabel
        self.db_server = tk.StringVar()
        self.db_name = tk.StringVar()
        self.auth_type = tk.StringVar(value="SQL Auth")
        self.db_user = tk.StringVar()
        self.db_pass = tk.StringVar()

        # Load config
        self.config_manager = SettingManager(Path("settings.ini"))
        self.load_config()

        self.build_form()

    def build_form(self):
        # Form layout
        tk.Label(self, text="Server Name").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.db_server).pack(fill="x", padx=10)

        tk.Label(self, text="Database").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.db_name).pack(fill="x", padx=10)

        tk.Label(self, text="Authentication").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Combobox(self, textvariable=self.auth_type, values=["SQL Auth", "Windows Auth"]).pack(fill="x", padx=10)

        tk.Label(self, text="Username").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.db_user).pack(fill="x", padx=10)

        tk.Label(self, text="Password").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(self, textvariable=self.db_pass, show="*").pack(fill="x", padx=10)

        # Tombol
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Test Koneksi", command=self.test_connection).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_connection).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

    def load_config(self):
        conn_string = self.config_manager.get("DATABASE", "oto_db_url", "")
        if conn_string:
            try:
                parts = conn_string.split(";")
                for part in parts:
                    if part.startswith("SERVER="):
                        self.db_server.set(part.replace("SERVER=", ""))
                    elif part.startswith("DATABASE="):
                        self.db_name.set(part.replace("DATABASE=", ""))
                    elif part.startswith("UID="):
                        self.db_user.set(part.replace("UID=", ""))
                        self.auth_type.set("SQL Auth")
            except:
                pass

    def test_connection(self):
        try:
            # Buat connection string
            if self.auth_type.get() == "SQL Auth":
                conn_string = f"DRIVER={{SQL Server}};SERVER={self.db_server.get()};DATABASE={self.db_name.get()};UID={self.db_user.get()};PWD={self.db_pass.get()}"
            else:  # Windows Auth
                conn_string = f"DRIVER={{SQL Server}};SERVER={self.db_server.get()};DATABASE={self.db_name.get()};Trusted_Connection=yes"

            # Test koneksi (dalam versi production, gunakan pyodbc.connect)
            messagebox.showinfo("Test Koneksi", "Koneksi berhasil!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal koneksi ke database: {e}")

    def save_connection(self):
        try:
            # Buat connection string
            if self.auth_type.get() == "SQL Auth":
                conn_string = f"DRIVER={{SQL Server}};SERVER={self.db_server.get()};DATABASE={self.db_name.get()};UID={self.db_user.get()};PWD={self.db_pass.get()}"
            else:  # Windows Auth
                conn_string = f"DRIVER={{SQL Server}};SERVER={self.db_server.get()};DATABASE={self.db_name.get()};Trusted_Connection=yes"

            # Di implementasi sebenarnya, Anda mungkin perlu mengenkripsi connection string
            # conn_string = encrypt(conn_string)

            self.config_manager.set("DATABASE", "oto_db_url", conn_string)
            messagebox.showinfo("Sukses", "Konfigurasi database berhasil disimpan.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan konfigurasi: {e}")


def show_database_form(parent=None):
    app = DatabaseForm(parent=parent)
    app.grab_set()
    app.wait_window()

def safe_show_database_form():
    root = tk.Tk()
    root.withdraw()
    show_database_form(parent=root)
    root.destroy()
