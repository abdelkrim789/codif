"""Insertion form with cascading dropdowns"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class InsertionWindow:
    """Window for adding new repair insertions"""
    
    def __init__(self, root, excel_mgr, on_success):
        self.root = root
        self.excel_mgr = excel_mgr
        self.on_success = on_success
        
        self.root.title("New Insertion")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Load reference data
        self.ref_data = excel_mgr.load_reference_data()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create form widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="New Repair Insertion",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=15)
        
        # Scrollable frame
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        row = 0
        
        # Client (free text)
        tk.Label(scrollable_frame, text="Client:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.client_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30)
        self.client_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Famille (dropdown)
        tk.Label(scrollable_frame, text="Famille:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.famille_var = tk.StringVar()
        self.famille_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.famille_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.famille_combo.grid(row=row, column=1, padx=10, pady=5)
        self.famille_combo.bind("<<ComboboxSelected>>", self.on_famille_selected)
        row += 1
        
        # Produit (cascading dropdown)
        tk.Label(scrollable_frame, text="Produit:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.produit_var = tk.StringVar()
        self.produit_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.produit_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.produit_combo.grid(row=row, column=1, padx=10, pady=5)
        self.produit_combo.bind("<<ComboboxSelected>>", self.on_produit_selected)
        row += 1
        
        # Type de produit / Model (cascading dropdown)
        tk.Label(scrollable_frame, text="Type de produit:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.model_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.model_combo.grid(row=row, column=1, padx=10, pady=5)
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_selected)
        row += 1
        
        # N° de série (free text)
        tk.Label(scrollable_frame, text="N° de série:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.num_serie_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30)
        self.num_serie_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Garantie (dropdown)
        tk.Label(scrollable_frame, text="Garantie:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.garantie_var = tk.StringVar()
        self.garantie_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.garantie_var,
            values=["Garantie", "Hors Garantie", "Fiche de garantie", "Non-conforme"],
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.garantie_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Date produit (date picker - will use Entry for simplicity)
        tk.Label(scrollable_frame, text="Date produit:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.date_produit_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30)
        self.date_produit_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_produit_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Panne (cascading dropdown)
        tk.Label(scrollable_frame, text="Panne:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.panne_var = tk.StringVar()
        self.panne_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.panne_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.panne_combo.grid(row=row, column=1, padx=10, pady=5)
        self.panne_combo.bind("<<ComboboxSelected>>", self.on_panne_selected)
        row += 1
        
        # Cause (cascading dropdown)
        tk.Label(scrollable_frame, text="Cause:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.cause_var = tk.StringVar()
        self.cause_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.cause_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.cause_combo.grid(row=row, column=1, padx=10, pady=5)
        self.cause_combo.bind("<<ComboboxSelected>>", self.on_cause_selected)
        row += 1
        
        # Réparation effectuée (auto-filled from solution)
        tk.Label(scrollable_frame, text="Réparation effectuée:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.reparation_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30, state="readonly")
        self.reparation_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # PDR consommée (dropdown)
        tk.Label(scrollable_frame, text="PDR consommée:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.pdr_var = tk.StringVar()
        self.pdr_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.pdr_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.pdr_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Statut (dropdown)
        tk.Label(scrollable_frame, text="Statut:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.statut_var = tk.StringVar()
        self.statut_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.statut_var,
            values=["Réparé", "En cours", "Non réparé", "Pièce non disponible", "Changé"],
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.statut_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Centre (dropdown)
        tk.Label(scrollable_frame, text="Centre:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.centre_var = tk.StringVar()
        self.centre_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.centre_var,
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.centre_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Date réception
        tk.Label(scrollable_frame, text="Date réception:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.date_reception_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30)
        self.date_reception_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_reception_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        # Date réparation
        tk.Label(scrollable_frame, text="Date réparation:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        self.date_reparation_entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=30)
        self.date_reparation_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_reparation_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.save_insertion
        )
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
            command=self.root.destroy
        )
        cancel_btn.pack(side="left", padx=5)
        
        # Initialize dropdowns
        self.populate_familles()
        self.populate_centres()
        self.populate_pdr()
    
    def populate_familles(self):
        """Populate famille dropdown"""
        familles = [f['famille'] for f in self.ref_data.get('familles', [])]
        self.famille_combo['values'] = familles
    
    def populate_centres(self):
        """Populate centres dropdown"""
        centres = [c['centre'] for c in self.ref_data.get('centres', [])]
        if not centres:
            centres = ['Centre Principal']  # Default if no centres
        self.centre_combo['values'] = centres
    
    def populate_pdr(self):
        """Populate PDR dropdown"""
        pdr_list = [p['pdr'] for p in self.ref_data.get('pdr', [])]
        if not pdr_list:
            pdr_list = ['N/A']  # Default if no PDR
        self.pdr_combo['values'] = pdr_list
    
    def on_famille_selected(self, event):
        """Handle famille selection"""
        famille_name = self.famille_var.get()
        famille = next((f for f in self.ref_data.get('familles', []) if f['famille'] == famille_name), None)
        
        if famille:
            # Filter produits by famille
            produits = [p['produit'] for p in self.ref_data.get('produits', []) if p['famille_id'] == famille['id']]
            self.produit_combo['values'] = produits
            self.produit_var.set('')
            self.model_var.set('')
            self.panne_var.set('')
            self.cause_var.set('')
    
    def on_produit_selected(self, event):
        """Handle produit selection"""
        produit_name = self.produit_var.get()
        produit = next((p for p in self.ref_data.get('produits', []) if p['produit'] == produit_name), None)
        
        if produit:
            # Filter models by produit
            models = [m['model'] for m in self.ref_data.get('models', []) if m['produit_id'] == produit['id']]
            self.model_combo['values'] = models
            self.model_var.set('')
            self.panne_var.set('')
            self.cause_var.set('')
            
            # Also populate pannes for this produit (in case model is not needed)
            pannes = [p['panne'] for p in self.ref_data.get('pannes', []) if p['produit_id'] == produit['id']]
            # Get unique pannes
            unique_pannes = list(dict.fromkeys(pannes))
            self.panne_combo['values'] = unique_pannes
    
    def on_model_selected(self, event):
        """Handle model selection"""
        # Models don't affect panne selection, but we keep the cascade
        pass
    
    def on_panne_selected(self, event):
        """Handle panne selection"""
        panne_name = self.panne_var.get()
        produit_name = self.produit_var.get()
        produit = next((p for p in self.ref_data.get('produits', []) if p['produit'] == produit_name), None)
        
        if produit:
            # Find panne for this produit
            panne = next((p for p in self.ref_data.get('pannes', []) 
                         if p['panne'] == panne_name and p['produit_id'] == produit['id']), None)
            
            if panne:
                # Filter causes by panne
                causes = [c['cause'] for c in self.ref_data.get('causes', []) if c['panne_id'] == panne['id']]
                self.cause_combo['values'] = causes
                self.cause_var.set('')
    
    def on_cause_selected(self, event):
        """Handle cause selection and auto-fill solution"""
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
                    # Find solution for this cause
                    solution = next((s for s in self.ref_data.get('solutions', []) 
                                   if s['cause_id'] == cause['id']), None)
                    
                    if solution:
                        # Auto-fill reparation field
                        self.reparation_entry.config(state="normal")
                        self.reparation_entry.delete(0, tk.END)
                        self.reparation_entry.insert(0, solution['solution'])
                        self.reparation_entry.config(state="readonly")
    
    def save_insertion(self):
        """Save the insertion"""
        # Validate required fields
        if not self.client_entry.get().strip():
            messagebox.showerror("Error", "Client is required")
            return
        
        if not self.produit_var.get():
            messagebox.showerror("Error", "Produit is required")
            return
        
        if not self.model_var.get():
            messagebox.showerror("Error", "Type de produit is required")
            return
        
        # Prepare insertion data
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
        
        # Save to Excel
        try:
            self.excel_mgr.add_insertion(insertion_data)
            self.root.destroy()
            self.on_success()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save insertion: {str(e)}")
