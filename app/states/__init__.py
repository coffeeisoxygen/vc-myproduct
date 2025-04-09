"""
State management untuk aplikasi vc-myproduct.

Modul ini mengelola berbagai state aplikasi seperti:
- State aplikasi secara keseluruhan
- State hardware dan identifikasi PC
- Koneksi database aplikasi (SQLite)
- Koneksi database Otomax
"""

from app.states.state_manager import AppState
from app.states.state_hardware import HardwareState

__all__ = ["AppState", "HardwareState"]
