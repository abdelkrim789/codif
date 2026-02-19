"""Formulaire d'insertion avec menus en cascade"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


COLORS = {
    'primary': '#1565C0',
    'primary_dark': '#0D47A1',
    'success': '#2E7D32',
    'danger': '#C62828',
    'bg': '#F5F5F5',
    'card_bg': '#FFFFFF',
    'text': '#212121',
    'border': '#E0E0E0',
    'header_bg': '#1565C0',
}


class InsertionWindow:
    """Fenêtre d'ajout de nouvelles insertions de réparation"""
    
    def __init__(self, root, excel_mgr, on_success):
        self.root = root
        self.excel_mgr = excel_mgr
        self.on_success = on_success
        
        self.root.title("Nouvelle Insertion")
        self.root.geometry("620x720")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg'])
        
        self.ref_data = excel_mgr.load_reference_data()
        self.create_widgets()
    
    def create_widgets(self):
        """Créer les widgets du formulaire"""
        # Header
        header = tk.Frame(self.root, bg=COLORS['header_bg'], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Nouvelle Insertion de Réparation",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORS['header_bg'], fg="white").pack(pady=10)
        
        # Scrollable card
        canvas = tk.Canvas(self.root, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        card = tk.Frame(canvas, bg=COLORS['card_bg'], bd=0)
        
        card.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((10, 10), window=card, anchor="nw", width=570)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        lbl_opts = {"font": ("Segoe UI", 10), "bg": COLORS['card_bg'], "fg": COLORS['text']}
        entry_opts = {"font": ("Segoe UI", 10), "width": 30, "relief": "solid", "bd": 1}
        combo_opts = {"font": ("Segoe UI", 10), "width": 28, "state": "readonly"}
        
        # Client
        tk.Label(card, text="Client :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.client_entry = tk.Entry(card, **entry_opts)
        self.client_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Famille
        tk.Label(card, text="Famille :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.famille_var = tk.StringVar()
        self.famille_combo = ttk.Combobox(card, textvariable=self.famille_var, **combo_opts)
        self.famille_combo.grid(row=row, column=1, padx=10, pady=6)
        self.famille_combo.bind("<<ComboboxSelected>>", self.on_famille_selected)
        row += 1
        
        # Produit
        tk.Label(card, text="Produit :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.produit_var = tk.StringVar()
        self.produit_combo = ttk.Combobox(card, textvariable=self.produit_var, **combo_opts)
        self.produit_combo.grid(row=row, column=1, padx=10, pady=6)
        self.produit_combo.bind("<<ComboboxSelected>>", self.on_produit_selected)
        row += 1
        
        # Type de produit
        tk.Label(card, text="Type de produit :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(card, textvariable=self.model_var, **combo_opts)
        self.model_combo.grid(row=row, column=1, padx=10, pady=6)
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_selected)
        row += 1
        
        # N° de série
        tk.Label(card, text="N° de série :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.num_serie_entry = tk.Entry(card, **entry_opts)
        self.num_serie_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Garantie
        tk.Label(card, text="Garantie :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.garantie_var = tk.StringVar()
        self.garantie_combo = ttk.Combobox(card, textvariable=self.garantie_var,
                                            values=["Garantie", "Hors Garantie", "Fiche de garantie", "Non-conforme"],
                                            **combo_opts)
        self.garantie_combo.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Date produit
        tk.Label(card, text="Date produit :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.date_produit_entry = tk.Entry(card, **entry_opts)
        self.date_produit_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_produit_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Panne
        tk.Label(card, text="Panne :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.panne_var = tk.StringVar()
        self.panne_combo = ttk.Combobox(card, textvariable=self.panne_var, **combo_opts)
        self.panne_combo.grid(row=row, column=1, padx=10, pady=6)
        self.panne_combo.bind("<<ComboboxSelected>>", self.on_panne_selected)
        row += 1
        
        # Cause
        tk.Label(card, text="Cause :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.cause_var = tk.StringVar()
        self.cause_combo = ttk.Combobox(card, textvariable=self.cause_var, **combo_opts)
        self.cause_combo.grid(row=row, column=1, padx=10, pady=6)
        self.cause_combo.bind("<<ComboboxSelected>>", self.on_cause_selected)
        row += 1
        
        # Réparation effectuée
        tk.Label(card, text="Réparation effectuée :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.reparation_entry = tk.Entry(card, font=("Segoe UI", 10), width=30, state="readonly",
                                          relief="solid", bd=1)
        self.reparation_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # PDR consommée
        tk.Label(card, text="PDR consommée :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.pdr_var = tk.StringVar()
        self.pdr_combo = ttk.Combobox(card, textvariable=self.pdr_var, **combo_opts)
        self.pdr_combo.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Statut
        tk.Label(card, text="Statut :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.statut_var = tk.StringVar()
        self.statut_combo = ttk.Combobox(card, textvariable=self.statut_var,
                                          values=["Réparé", "En cours", "Non réparé",
                                                  "Pièce non disponible", "Changé"],
                                          **combo_opts)
        self.statut_combo.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Centre
        tk.Label(card, text="Centre :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.centre_var = tk.StringVar()
        self.centre_combo = ttk.Combobox(card, textvariable=self.centre_var, **combo_opts)
        self.centre_combo.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Date réception
        tk.Label(card, text="Date réception :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.date_reception_entry = tk.Entry(card, **entry_opts)
        self.date_reception_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_reception_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        # Date réparation
        tk.Label(card, text="Date réparation :", **lbl_opts).grid(row=row, column=0, sticky="e", padx=10, pady=6)
        self.date_reparation_entry = tk.Entry(card, **entry_opts)
        self.date_reparation_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_reparation_entry.grid(row=row, column=1, padx=10, pady=6)
        row += 1
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLORS['bg'])
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Enregistrer", font=("Segoe UI", 11, "bold"),
                  bg=COLORS['success'], fg="white", width=14, relief="flat",
                  cursor="hand2", command=self.save_insertion).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Annuler", font=("Segoe UI", 11),
                  bg=COLORS['danger'], fg="white", width=14, relief="flat",
                  cursor="hand2", command=self.root.destroy).pack(side="left", padx=5)
        
        # Init dropdowns
        self.populate_familles()
        self.populate_centres()
        self.populate_pdr()
    
    def populate_familles(self):
        familles = [f['famille'] for f in self.ref_data.get('familles', [])]
        self.famille_combo['values'] = familles
    
    def populate_centres(self):
        """Remplir la liste des centres et agents agréés"""
        options = []
        for c in self.ref_data.get('centres', []):
            options.append(c['centre'])
        for a in self.ref_data.get('agents', []):
            label = f"Agent: {a['nom_prenom']}"
            if a.get('wilaya'):
                label += f" - {a['wilaya']}"
            options.append(label)
        if not options:
            options = ['Centre Principal']
        self.centre_combo['values'] = options
    
    def populate_pdr(self):
        pdr_list = [p['pdr'] for p in self.ref_data.get('pdr', [])]
        if not pdr_list:
            pdr_list = ['N/A']
        self.pdr_combo['values'] = pdr_list
    
    def on_famille_selected(self, event):
        famille_name = self.famille_var.get()
        famille = next((f for f in self.ref_data.get('familles', []) if f['famille'] == famille_name), None)
        if famille:
            produits = [p['produit'] for p in self.ref_data.get('produits', []) if p['famille_id'] == famille['id']]
            self.produit_combo['values'] = produits
            self.produit_var.set('')
            self.model_var.set('')
            self.panne_var.set('')
            self.cause_var.set('')
    
    def on_produit_selected(self, event):
        produit_name = self.produit_var.get()
        produit = next((p for p in self.ref_data.get('produits', []) if p['produit'] == produit_name), None)
        if produit:
            models = [m['model'] for m in self.ref_data.get('models', []) if m['produit_id'] == produit['id']]
            self.model_combo['values'] = models
            self.model_var.set('')
            self.panne_var.set('')
            self.cause_var.set('')
            pannes = [p['panne'] for p in self.ref_data.get('pannes', []) if p['produit_id'] == produit['id']]
            self.panne_combo['values'] = list(dict.fromkeys(pannes))
    
    def on_model_selected(self, event):
        pass
    
    def on_panne_selected(self, event):
        panne_name = self.panne_var.get()
        produit_name = self.produit_var.get()
        produit = next((p for p in self.ref_data.get('produits', []) if p['produit'] == produit_name), None)
        if produit:
            panne = next((p for p in self.ref_data.get('pannes', [])
                         if p['panne'] == panne_name and p['produit_id'] == produit['id']), None)
            if panne:
                causes = [c['cause'] for c in self.ref_data.get('causes', []) if c['panne_id'] == panne['id']]
                self.cause_combo['values'] = causes
                self.cause_var.set('')
    
    def on_cause_selected(self, event):
        cause_name = self.cause_var.get()
        panne_name = self.panne_var.get()
        produit_name = self.produit_var.get()
        produit = next((p for p in self.ref_data.get('produits', []) if p['produit'] == produit_name), None)
        if produit:
            panne = next((p for p in self.ref_data.get('pannes', [])
                         if p['panne'] == panne_name and p['produit_id'] == produit['id']), None)
            if panne:
                cause = next((c for c in self.ref_data.get('causes', [])
                             if c['cause'] == cause_name and c['panne_id'] == panne['id']), None)
                if cause:
                    solution = next((s for s in self.ref_data.get('solutions', [])
                                   if s['cause_id'] == cause['id']), None)
                    if solution:
                        self.reparation_entry.config(state="normal")
                        self.reparation_entry.delete(0, tk.END)
                        self.reparation_entry.insert(0, solution['solution'])
                        self.reparation_entry.config(state="readonly")
    
    def save_insertion(self):
        if not self.client_entry.get().strip():
            messagebox.showerror("Erreur", "Le champ Client est obligatoire")
            return
        if not self.produit_var.get():
            messagebox.showerror("Erreur", "Le champ Produit est obligatoire")
            return
        if not self.model_var.get():
            messagebox.showerror("Erreur", "Le champ Type de produit est obligatoire")
            return
        
        insertion_data = {
            'client': self.client_entry.get().strip(),
            'produit': self.produit_var.get(),
            'type_produit': self.model_var.get(),
            'num_serie': self.num_serie_entry.get().strip(),
            'garantie': self.garantie_var.get(),
            'date_produit': self.date_produit_entry.get().strip(),
            'panne': self.panne_var.get(),
            'reparation': self.reparation_entry.get(),
            'pdr': self.pdr_var.get(),
            'statut': self.statut_var.get(),
            'centre': self.centre_var.get(),
            'date_reception': self.date_reception_entry.get().strip(),
            'date_reparation': self.date_reparation_entry.get().strip()
        }
        
        try:
            self.excel_mgr.add_insertion(insertion_data)
            self.root.destroy()
            self.on_success()
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'enregistrement : {str(e)}")
