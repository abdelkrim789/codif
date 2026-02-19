"""Main entry point for the SAV Repair Data Management Application"""
import tkinter as tk
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.gui.login import LoginWindow
from app.gui.dashboard import Dashboard


def on_login_success(auth_mgr):
    """Callback when login is successful"""
    # Create main window
    root = tk.Tk()
    Dashboard(root, auth_mgr)
    root.mainloop()


def main():
    """Main application entry point"""
    # Create login window
    root = tk.Tk()
    LoginWindow(root, on_login_success)
    root.mainloop()


if __name__ == '__main__':
    main()
