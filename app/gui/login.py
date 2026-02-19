"""Écran de connexion de l'application"""
import tkinter as tk
from tkinter import messagebox
from app.auth import AuthManager


# Modern color palette
COLORS = {
    'primary': '#1565C0',       # Deep blue
    'primary_dark': '#0D47A1',  # Darker blue
    'primary_light': '#1976D2', # Lighter blue
    'accent': '#00897B',        # Teal
    'success': '#2E7D32',       # Green
    'danger': '#C62828',        # Red
    'warning': '#EF6C00',       # Orange
    'bg': '#F5F5F5',            # Light grey bg
    'card_bg': '#FFFFFF',       # Card background
    'text': '#212121',          # Dark text
    'text_light': '#757575',    # Light text
    'border': '#E0E0E0',       # Border color
}


class LoginWindow:
    """Fenêtre de connexion utilisateur"""
    
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.auth_mgr = AuthManager()
        
        self.root.title("Gestion SAV - Connexion")
        self.root.geometry("450x380")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg'])
        
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = 450
        height = 380
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Créer les widgets du formulaire de connexion"""
        # Header band
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Gestion SAV",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['primary'],
            fg="white"
        ).pack(pady=10)
        tk.Label(
            header,
            text="Système de gestion des réparations",
            font=("Segoe UI", 10),
            bg=COLORS['primary'],
            fg="#BBDEFB"
        ).pack()
        
        # Card
        card = tk.Frame(self.root, bg=COLORS['card_bg'], bd=0, relief="flat",
                        highlightbackground=COLORS['border'], highlightthickness=1)
        card.place(relx=0.5, rely=0.58, anchor="center", width=360, height=230)
        
        tk.Label(
            card, text="Connexion", font=("Segoe UI", 14, "bold"),
            bg=COLORS['card_bg'], fg=COLORS['text']
        ).pack(pady=(15, 10))
        
        # Form
        form = tk.Frame(card, bg=COLORS['card_bg'])
        form.pack(pady=5)
        
        tk.Label(form, text="Nom d'utilisateur :", font=("Segoe UI", 10),
                 bg=COLORS['card_bg'], fg=COLORS['text']).grid(row=0, column=0, sticky="e", padx=8, pady=8)
        self.username_entry = tk.Entry(form, font=("Segoe UI", 11), width=20,
                                       relief="solid", bd=1)
        self.username_entry.grid(row=0, column=1, padx=8, pady=8)
        self.username_entry.focus()
        
        tk.Label(form, text="Mot de passe :", font=("Segoe UI", 10),
                 bg=COLORS['card_bg'], fg=COLORS['text']).grid(row=1, column=0, sticky="e", padx=8, pady=8)
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), width=20, show="●",
                                       relief="solid", bd=1)
        self.password_entry.grid(row=1, column=1, padx=8, pady=8)
        
        # Bind Enter
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(
            card, text="Se connecter", font=("Segoe UI", 11, "bold"),
            bg=COLORS['primary'], fg="white", activebackground=COLORS['primary_dark'],
            activeforeground="white", width=20, relief="flat", cursor="hand2",
            command=self.login
        )
        login_btn.pack(pady=15)
    
    def login(self):
        """Gérer le clic sur le bouton de connexion"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez saisir le nom d'utilisateur et le mot de passe")
            return
        
        user = self.auth_mgr.authenticate(username, password)
        if user:
            self.root.destroy()
            self.on_success(self.auth_mgr)
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe invalide")
            self.password_entry.delete(0, tk.END)
