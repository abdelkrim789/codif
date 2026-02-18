"""Login screen for the application"""
import tkinter as tk
from tkinter import messagebox
from app.auth import AuthManager


class LoginWindow:
    """Login window for user authentication"""
    
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.auth_mgr = AuthManager()
        
        self.root.title("SAV Repair Data - Login")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create login form widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="SAV Repair Data Management",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # Frame for form
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        
        # Username
        username_label = tk.Label(form_frame, text="Username:", font=("Arial", 11))
        username_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        
        self.username_entry = tk.Entry(form_frame, font=("Arial", 11), width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.username_entry.focus()
        
        # Password
        password_label = tk.Label(form_frame, text="Password:", font=("Arial", 11))
        password_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        
        self.password_entry = tk.Entry(form_frame, font=("Arial", 11), width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(
            self.root,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.login
        )
        login_btn.pack(pady=20)
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        user = self.auth_mgr.authenticate(username, password)
        if user:
            self.root.destroy()
            self.on_success(self.auth_mgr)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
