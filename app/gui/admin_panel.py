"""Admin panel for CRUD operations with Excel import, Agents Agréés, and Archives"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog


class AdminPanel:
    """Admin panel for managing reference data"""
    
    def __init__(self, root, excel_mgr):
        self.root = root
        self.excel_mgr = excel_mgr
        
        self.root.title("Admin Panel")
        self.root.geometry("1000x650")
        
        # Load reference data
        self.ref_data = excel_mgr.load_reference_data()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create admin panel widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="Administration Panel",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_familles_tab(notebook)
        self.create_produits_tab(notebook)
        self.create_models_tab(notebook)
        self.create_pannes_tab(notebook)
        self.create_causes_tab(notebook)
        self.create_solutions_tab(notebook)
        self.create_centres_tab(notebook)
        self.create_agents_tab(notebook)
        self.create_users_tab(notebook)
        self.create_import_tab(notebook)
        self.create_archives_tab(notebook)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="Save All Changes",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.save_changes
        )
        save_btn.pack(side="left", padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=15,
            command=self.root.destroy
        )
        close_btn.pack(side="left", padx=5)
    
    # ---- Familles Tab ----
    def create_familles_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Familles")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_famille).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.familles_tree, 'familles')).pack(side="left", padx=2)
        
        self.familles_tree = ttk.Treeview(frame, columns=('ID', 'Famille'), show='headings')
        self.familles_tree.heading('ID', text='ID')
        self.familles_tree.heading('Famille', text='Famille')
        self.familles_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for f in self.ref_data.get('familles', []):
            self.familles_tree.insert('', 'end', values=(f['id'], f['famille']))
    
    # ---- Produits Tab ----
    def create_produits_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Produits")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_produit).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.produits_tree, 'produits')).pack(side="left", padx=2)
        
        self.produits_tree = ttk.Treeview(frame, columns=('ID', 'Famille ID', 'Produit'), show='headings')
        self.produits_tree.heading('ID', text='ID')
        self.produits_tree.heading('Famille ID', text='Famille ID')
        self.produits_tree.heading('Produit', text='Produit')
        self.produits_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for p in self.ref_data.get('produits', []):
            self.produits_tree.insert('', 'end', values=(p['id'], p['famille_id'], p['produit']))
    
    # ---- Models Tab ----
    def create_models_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Models")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_model).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.models_tree, 'models')).pack(side="left", padx=2)
        
        self.models_tree = ttk.Treeview(frame, columns=('ID', 'Produit ID', 'Model'), show='headings')
        self.models_tree.heading('ID', text='ID')
        self.models_tree.heading('Produit ID', text='Produit ID')
        self.models_tree.heading('Model', text='Model')
        self.models_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for m in self.ref_data.get('models', []):
            self.models_tree.insert('', 'end', values=(m['id'], m['produit_id'], m['model']))
    
    # ---- Pannes Tab ----
    def create_pannes_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Pannes")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_panne).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.pannes_tree, 'pannes')).pack(side="left", padx=2)
        
        self.pannes_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Produit ID', 'Panne'), show='headings')
        self.pannes_tree.heading('ID', text='ID')
        self.pannes_tree.heading('Code', text='Code')
        self.pannes_tree.heading('Produit ID', text='Produit ID')
        self.pannes_tree.heading('Panne', text='Panne')
        self.pannes_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for p in self.ref_data.get('pannes', []):
            self.pannes_tree.insert('', 'end', values=(p['id'], p['code'], p['produit_id'], p['panne']))
    
    # ---- Causes Tab ----
    def create_causes_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Causes")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_cause).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.causes_tree, 'causes')).pack(side="left", padx=2)
        
        self.causes_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Panne ID', 'Cause'), show='headings')
        self.causes_tree.heading('ID', text='ID')
        self.causes_tree.heading('Code', text='Code')
        self.causes_tree.heading('Panne ID', text='Panne ID')
        self.causes_tree.heading('Cause', text='Cause')
        self.causes_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for c in self.ref_data.get('causes', []):
            self.causes_tree.insert('', 'end', values=(c['id'], c['code'], c['panne_id'], c['cause']))
    
    # ---- Solutions Tab ----
    def create_solutions_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Solutions")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add", command=self.add_solution).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.solutions_tree, 'solutions')).pack(side="left", padx=2)
        
        self.solutions_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Cause ID', 'Solution'), show='headings')
        self.solutions_tree.heading('ID', text='ID')
        self.solutions_tree.heading('Code', text='Code')
        self.solutions_tree.heading('Cause ID', text='Cause ID')
        self.solutions_tree.heading('Solution', text='Solution')
        self.solutions_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for s in self.ref_data.get('solutions', []):
            self.solutions_tree.insert('', 'end', values=(s['id'], s['code'], s['cause_id'], s['solution']))
    
    # ---- Centres Tab ----
    def create_centres_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Centres")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add Centre", command=self.add_centre).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.centres_tree, 'centres')).pack(side="left", padx=2)
        
        self.centres_tree = ttk.Treeview(frame, columns=('ID', 'Centre'), show='headings')
        self.centres_tree.heading('ID', text='ID')
        self.centres_tree.heading('Centre', text='Centre')
        self.centres_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for c in self.ref_data.get('centres', []):
            self.centres_tree.insert('', 'end', values=(c['id'], c['centre']))
    
    # ---- Agents Agréés Tab ----
    def create_agents_tab(self, notebook):
        """Create agents agréés management tab with full input fields"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Agents Agréés")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add Agent", command=self.add_agent).pack(side="left", padx=2)
        tk.Button(toolbar, text="Import Agents from Excel",
                  command=self.import_agents_excel).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete",
                  command=lambda: self.delete_selected(self.agents_tree, 'agents')).pack(side="left", padx=2)
        
        # Inline form
        form_frame = tk.LabelFrame(frame, text="Add New Agent Agréé", padx=10, pady=5)
        form_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(form_frame, text="Nom et Prénom:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.agent_nom_entry = tk.Entry(form_frame, width=25)
        self.agent_nom_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(form_frame, text="Téléphone:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
        self.agent_tel_entry = tk.Entry(form_frame, width=18)
        self.agent_tel_entry.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(form_frame, text="Wilaya:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.agent_wilaya_entry = tk.Entry(form_frame, width=25)
        self.agent_wilaya_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(form_frame, text="Adresse:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.agent_adresse_entry = tk.Entry(form_frame, width=18)
        self.agent_adresse_entry.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(form_frame, text="+ Add", bg="#4CAF50", fg="white",
                  command=self.add_agent_from_form).grid(row=0, column=4, rowspan=2, padx=10, pady=2)
        
        # Tree
        self.agents_tree = ttk.Treeview(
            frame,
            columns=('ID', 'Nom Prénom', 'Téléphone', 'Wilaya', 'Adresse'),
            show='headings'
        )
        self.agents_tree.heading('ID', text='ID')
        self.agents_tree.heading('Nom Prénom', text='Nom et Prénom')
        self.agents_tree.heading('Téléphone', text='Téléphone')
        self.agents_tree.heading('Wilaya', text='Wilaya')
        self.agents_tree.heading('Adresse', text='Adresse')
        self.agents_tree.column('ID', width=40)
        self.agents_tree.column('Nom Prénom', width=180)
        self.agents_tree.column('Téléphone', width=120)
        self.agents_tree.column('Wilaya', width=120)
        self.agents_tree.column('Adresse', width=200)
        self.agents_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for a in self.ref_data.get('agents', []):
            self.agents_tree.insert('', 'end', values=(
                a['id'], a['nom_prenom'], a['telephone'], a['wilaya'], a['adresse']
            ))
    
    # ---- Users Tab ----
    def create_users_tab(self, notebook):
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Users")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Add User", command=self.add_user).pack(side="left", padx=2)
        tk.Button(toolbar, text="Reset Password", command=self.reset_password).pack(side="left", padx=2)
        tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.users_tree, 'users')).pack(side="left", padx=2)
        
        self.users_tree = ttk.Treeview(frame, columns=('ID', 'Username', 'Role'), show='headings')
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Username', text='Username')
        self.users_tree.heading('Role', text='Role')
        self.users_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for u in self.ref_data.get('users', []):
            self.users_tree.insert('', 'end', values=(u['id'], u['username'], u['role']))
    
    # ---- Import Data Tab ----
    def create_import_tab(self, notebook):
        """Tab for bulk Excel data import"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Import Data")
        
        # Reference data import
        info_frame = tk.LabelFrame(frame, text="Import Reference Data from Excel", padx=15, pady=10)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=(
            "Import data from an Excel file with matching sheet structure.\n"
            "The Excel file can contain any of these sheets:\n"
            "  Familles (ID, Famille)  |  Produits (ID, Famille_ID, Produit)\n"
            "  Models (ID, Produit_ID, Model)  |  Pannes (ID, Code, Produit_ID, Panne)\n"
            "  Causes (ID, Code, Panne_ID, Cause)  |  Solutions (ID, Code, Cause_ID, Solution)\n"
            "  PDR (ID, Code, PDR)  |  Centres (ID, Centre)\n"
            "  Agents (ID, Nom_Prenom, Telephone, Wilaya, Adresse)\n\n"
            "Data will be merged into existing data with new auto-generated IDs."
        ), font=("Arial", 10), justify="left").pack(anchor="w")
        
        tk.Button(
            info_frame,
            text="Select Excel File & Import All Data",
            font=("Arial", 11, "bold"),
            bg="#2196F3", fg="white",
            command=self.import_reference_excel
        ).pack(pady=10)
        
        # Agents import
        agents_frame = tk.LabelFrame(frame, text="Import Agents Agréés from Excel", padx=15, pady=10)
        agents_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(agents_frame, text=(
            "Import agents from a simple Excel file with columns:\n"
            "  Nom_Prenom | Telephone | Wilaya | Adresse\n"
            "(First row should be a header row)"
        ), font=("Arial", 10), justify="left").pack(anchor="w")
        
        tk.Button(
            agents_frame,
            text="Select Excel File & Import Agents",
            font=("Arial", 11, "bold"),
            bg="#FF9800", fg="white",
            command=self.import_agents_excel
        ).pack(pady=10)
        
        # Status log
        self.import_status = tk.Text(frame, height=8, state="disabled", font=("Courier", 9))
        self.import_status.pack(fill="both", expand=True, padx=10, pady=5)
    
    # ---- Archives Tab ----
    def create_archives_tab(self, notebook):
        """Tab for importing and viewing previous monthly reports"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Archives")
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        tk.Button(toolbar, text="Import Report to Archive", bg="#2196F3", fg="white",
                  command=self.import_archive).pack(side="left", padx=5)
        tk.Button(toolbar, text="Refresh", command=self.refresh_archives).pack(side="left", padx=5)
        tk.Button(toolbar, text="View Selected", command=self.view_archive).pack(side="left", padx=5)
        
        # Archives list
        self.archives_tree = ttk.Treeview(frame, columns=('Filename', 'Date', 'Size'), show='headings')
        self.archives_tree.heading('Filename', text='Filename')
        self.archives_tree.heading('Date', text='Date')
        self.archives_tree.heading('Size', text='Size')
        self.archives_tree.column('Filename', width=350)
        self.archives_tree.column('Date', width=150)
        self.archives_tree.column('Size', width=100)
        self.archives_tree.pack(fill="x", padx=5, pady=5)
        
        # Preview area
        tk.Label(frame, text="Archive Preview:", font=("Arial", 10, "bold"), anchor="w").pack(fill="x", padx=5)
        
        preview_frame = tk.Frame(frame)
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scroll_y = ttk.Scrollbar(preview_frame)
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(preview_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.archive_preview_tree = ttk.Treeview(
            preview_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.archive_preview_tree.pack(fill="both", expand=True)
        scroll_y.config(command=self.archive_preview_tree.yview)
        scroll_x.config(command=self.archive_preview_tree.xview)
        
        columns = ('#', 'Client', 'Produit', 'Type', 'N° série', 'Garantie',
                   'Date prod.', 'Panne', 'Réparation', 'PDR', 'Statut',
                   'Centre', 'Date réc.', 'Date rép.')
        self.archive_preview_tree['columns'] = columns
        self.archive_preview_tree['show'] = 'headings'
        for col in columns:
            self.archive_preview_tree.heading(col, text=col)
            self.archive_preview_tree.column(col, width=90)
        
        self.refresh_archives()
    
    # ==============================================================
    # CRUD Actions
    # ==============================================================
    
    def add_famille(self):
        name = simpledialog.askstring("Add Famille", "Enter famille name:")
        if name:
            new_id = max([f['id'] for f in self.ref_data['familles']], default=0) + 1
            self.ref_data['familles'].append({'id': new_id, 'famille': name})
            self.familles_tree.insert('', 'end', values=(new_id, name))
    
    def add_produit(self):
        famille_id = simpledialog.askinteger("Add Produit", "Enter Famille ID:")
        if famille_id:
            name = simpledialog.askstring("Add Produit", "Enter produit name:")
            if name:
                new_id = max([p['id'] for p in self.ref_data['produits']], default=0) + 1
                self.ref_data['produits'].append({'id': new_id, 'famille_id': famille_id, 'produit': name})
                self.produits_tree.insert('', 'end', values=(new_id, famille_id, name))
    
    def add_model(self):
        produit_id = simpledialog.askinteger("Add Model", "Enter Produit ID:")
        if produit_id:
            name = simpledialog.askstring("Add Model", "Enter model name:")
            if name:
                new_id = max([m['id'] for m in self.ref_data['models']], default=0) + 1
                self.ref_data['models'].append({'id': new_id, 'produit_id': produit_id, 'model': name})
                self.models_tree.insert('', 'end', values=(new_id, produit_id, name))
    
    def add_panne(self):
        produit_id = simpledialog.askinteger("Add Panne", "Enter Produit ID:")
        if produit_id:
            code = simpledialog.askstring("Add Panne", "Enter panne code:")
            if code:
                name = simpledialog.askstring("Add Panne", "Enter panne name:")
                if name:
                    new_id = max([p['id'] for p in self.ref_data['pannes']], default=0) + 1
                    self.ref_data['pannes'].append({'id': new_id, 'code': code, 'produit_id': produit_id, 'panne': name})
                    self.pannes_tree.insert('', 'end', values=(new_id, code, produit_id, name))
    
    def add_cause(self):
        panne_id = simpledialog.askinteger("Add Cause", "Enter Panne ID:")
        if panne_id:
            code = simpledialog.askstring("Add Cause", "Enter cause code:")
            if code:
                name = simpledialog.askstring("Add Cause", "Enter cause name:")
                if name:
                    new_id = max([c['id'] for c in self.ref_data['causes']], default=0) + 1
                    self.ref_data['causes'].append({'id': new_id, 'code': code, 'panne_id': panne_id, 'cause': name})
                    self.causes_tree.insert('', 'end', values=(new_id, code, panne_id, name))
    
    def add_solution(self):
        cause_id = simpledialog.askinteger("Add Solution", "Enter Cause ID:")
        if cause_id:
            code = simpledialog.askstring("Add Solution", "Enter solution code:")
            if code:
                name = simpledialog.askstring("Add Solution", "Enter solution name:")
                if name:
                    new_id = max([s['id'] for s in self.ref_data['solutions']], default=0) + 1
                    self.ref_data['solutions'].append({'id': new_id, 'code': code, 'cause_id': cause_id, 'solution': name})
                    self.solutions_tree.insert('', 'end', values=(new_id, code, cause_id, name))
    
    def add_centre(self):
        """Add new centre (just the name)"""
        name = simpledialog.askstring("Add Centre", "Enter centre name (e.g. Centre BBA):")
        if name:
            new_id = max([c['id'] for c in self.ref_data['centres']], default=0) + 1
            self.ref_data['centres'].append({'id': new_id, 'centre': name})
            self.centres_tree.insert('', 'end', values=(new_id, name))
    
    def add_agent(self):
        """Add new agent agréé via dialog prompts"""
        nom = simpledialog.askstring("Add Agent Agréé", "Nom et Prénom:")
        if nom:
            tel = simpledialog.askstring("Add Agent Agréé", "Téléphone:") or ''
            wilaya = simpledialog.askstring("Add Agent Agréé", "Wilaya:") or ''
            adresse = simpledialog.askstring("Add Agent Agréé", "Adresse:") or ''
            
            new_id = max([a['id'] for a in self.ref_data.get('agents', [])], default=0) + 1
            new_agent = {'id': new_id, 'nom_prenom': nom, 'telephone': tel, 'wilaya': wilaya, 'adresse': adresse}
            if 'agents' not in self.ref_data:
                self.ref_data['agents'] = []
            self.ref_data['agents'].append(new_agent)
            self.agents_tree.insert('', 'end', values=(new_id, nom, tel, wilaya, adresse))
    
    def add_agent_from_form(self):
        """Add agent from the inline form fields"""
        nom = self.agent_nom_entry.get().strip()
        if not nom:
            messagebox.showwarning("Warning", "Nom et Prénom is required")
            return
        
        tel = self.agent_tel_entry.get().strip()
        wilaya = self.agent_wilaya_entry.get().strip()
        adresse = self.agent_adresse_entry.get().strip()
        
        new_id = max([a['id'] for a in self.ref_data.get('agents', [])], default=0) + 1
        new_agent = {'id': new_id, 'nom_prenom': nom, 'telephone': tel, 'wilaya': wilaya, 'adresse': adresse}
        if 'agents' not in self.ref_data:
            self.ref_data['agents'] = []
        self.ref_data['agents'].append(new_agent)
        self.agents_tree.insert('', 'end', values=(new_id, nom, tel, wilaya, adresse))
        
        # Clear form
        self.agent_nom_entry.delete(0, tk.END)
        self.agent_tel_entry.delete(0, tk.END)
        self.agent_wilaya_entry.delete(0, tk.END)
        self.agent_adresse_entry.delete(0, tk.END)
    
    def add_user(self):
        username = simpledialog.askstring("Add User", "Enter username:")
        if username:
            password = simpledialog.askstring("Add User", "Enter password:")
            if password:
                role = simpledialog.askstring("Add User", "Enter role (admin/inserter):")
                if role in ['admin', 'inserter']:
                    new_id = max([u['id'] for u in self.ref_data['users']], default=0) + 1
                    self.ref_data['users'].append({'id': new_id, 'username': username, 'password': password, 'role': role})
                    self.users_tree.insert('', 'end', values=(new_id, username, role))
    
    def reset_password(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user")
            return
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        new_password = simpledialog.askstring("Reset Password", "Enter new password:")
        if new_password:
            for user in self.ref_data['users']:
                if user['id'] == user_id:
                    user['password'] = new_password
                    messagebox.showinfo("Success", "Password reset successfully")
                    break
    
    def delete_selected(self, tree, data_key):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item = tree.item(selection[0])
            item_id = item['values'][0]
            self.ref_data[data_key] = [x for x in self.ref_data[data_key] if x['id'] != item_id]
            tree.delete(selection[0])
    
    def save_changes(self):
        try:
            self.excel_mgr.save_reference_data(self.ref_data)
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
    
    # ==============================================================
    # Import Actions
    # ==============================================================
    
    def _log_import(self, message):
        self.import_status.config(state="normal")
        self.import_status.insert(tk.END, message + "\n")
        self.import_status.see(tk.END)
        self.import_status.config(state="disabled")
    
    def import_reference_excel(self):
        """Import reference data from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Reference Data Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return
        
        self._log_import(f"Importing from: {file_path}")
        success, message = self.excel_mgr.import_reference_from_excel(file_path)
        self._log_import(message)
        
        if success:
            self.ref_data = self.excel_mgr.load_reference_data()
            self._refresh_all_trees()
            messagebox.showinfo("Import Success", message)
        else:
            messagebox.showerror("Import Error", message)
    
    def import_agents_excel(self):
        """Import agents agréés from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Agents Agréés Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return
        
        if hasattr(self, 'import_status'):
            self._log_import(f"Importing agents from: {file_path}")
        
        success, message = self.excel_mgr.import_agents_from_excel(file_path)
        
        if hasattr(self, 'import_status'):
            self._log_import(message)
        
        if success:
            self.ref_data = self.excel_mgr.load_reference_data()
            self._refresh_agents_tree()
            messagebox.showinfo("Import Success", message)
        else:
            messagebox.showerror("Import Error", message)
    
    def _refresh_all_trees(self):
        """Refresh all treeview widgets after data reload"""
        for item in self.familles_tree.get_children():
            self.familles_tree.delete(item)
        for f in self.ref_data.get('familles', []):
            self.familles_tree.insert('', 'end', values=(f['id'], f['famille']))
        
        for item in self.produits_tree.get_children():
            self.produits_tree.delete(item)
        for p in self.ref_data.get('produits', []):
            self.produits_tree.insert('', 'end', values=(p['id'], p['famille_id'], p['produit']))
        
        for item in self.models_tree.get_children():
            self.models_tree.delete(item)
        for m in self.ref_data.get('models', []):
            self.models_tree.insert('', 'end', values=(m['id'], m['produit_id'], m['model']))
        
        for item in self.pannes_tree.get_children():
            self.pannes_tree.delete(item)
        for p in self.ref_data.get('pannes', []):
            self.pannes_tree.insert('', 'end', values=(p['id'], p['code'], p['produit_id'], p['panne']))
        
        for item in self.causes_tree.get_children():
            self.causes_tree.delete(item)
        for c in self.ref_data.get('causes', []):
            self.causes_tree.insert('', 'end', values=(c['id'], c['code'], c['panne_id'], c['cause']))
        
        for item in self.solutions_tree.get_children():
            self.solutions_tree.delete(item)
        for s in self.ref_data.get('solutions', []):
            self.solutions_tree.insert('', 'end', values=(s['id'], s['code'], s['cause_id'], s['solution']))
        
        for item in self.centres_tree.get_children():
            self.centres_tree.delete(item)
        for c in self.ref_data.get('centres', []):
            self.centres_tree.insert('', 'end', values=(c['id'], c['centre']))
        
        self._refresh_agents_tree()
        
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        for u in self.ref_data.get('users', []):
            self.users_tree.insert('', 'end', values=(u['id'], u['username'], u['role']))
    
    def _refresh_agents_tree(self):
        for item in self.agents_tree.get_children():
            self.agents_tree.delete(item)
        for a in self.ref_data.get('agents', []):
            self.agents_tree.insert('', 'end', values=(
                a['id'], a['nom_prenom'], a['telephone'], a['wilaya'], a['adresse']
            ))
    
    # ==============================================================
    # Archive Actions
    # ==============================================================
    
    def refresh_archives(self):
        for item in self.archives_tree.get_children():
            self.archives_tree.delete(item)
        for arc in self.excel_mgr.list_archives():
            size_kb = f"{arc['size'] / 1024:.1f} KB"
            self.archives_tree.insert('', 'end', values=(arc['filename'], arc['date'], size_kb))
    
    def import_archive(self):
        file_path = filedialog.askopenfilename(
            title="Select Monthly Report to Archive",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return
        success, message = self.excel_mgr.import_archive(file_path)
        if success:
            self.refresh_archives()
            messagebox.showinfo("Archive Success", message)
        else:
            messagebox.showerror("Archive Error", message)
    
    def view_archive(self):
        selection = self.archives_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an archive to view")
            return
        
        item = self.archives_tree.item(selection[0])
        filename = item['values'][0]
        archive_path = os.path.join(self.excel_mgr.archives_dir, filename)
        
        for child in self.archive_preview_tree.get_children():
            self.archive_preview_tree.delete(child)
        
        insertions = self.excel_mgr.load_archive_data(archive_path)
        if not insertions:
            messagebox.showinfo("Info", "No data found in this archive")
            return
        
        for ins in insertions:
            self.archive_preview_tree.insert('', 'end', values=(
                ins.get('num', ''), ins.get('client', ''), ins.get('produit', ''),
                ins.get('type_produit', ''), ins.get('num_serie', ''), ins.get('garantie', ''),
                ins.get('date_produit', ''), ins.get('panne', ''), ins.get('reparation', ''),
                ins.get('pdr', ''), ins.get('statut', ''), ins.get('centre', ''),
                ins.get('date_reception', ''), ins.get('date_reparation', '')
            ))
