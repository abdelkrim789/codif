"""Panneau d'administration avec opérations CRUD, import Excel, Agents Agréés et Archives"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog


COLORS = {
    'primary': '#1565C0',
    'primary_dark': '#0D47A1',
    'success': '#2E7D32',
    'danger': '#C62828',
    'warning': '#EF6C00',
    'bg': '#F5F5F5',
    'card_bg': '#FFFFFF',
    'text': '#212121',
    'text_light': '#757575',
    'border': '#E0E0E0',
    'header_bg': '#1565C0',
    'toolbar_bg': '#FAFAFA',
    'filter_bg': '#E3F2FD',
}


class AdminPanel:
    """Panneau d'administration pour gérer les données de référence"""
    
    def __init__(self, root, excel_mgr):
        self.root = root
        self.excel_mgr = excel_mgr
        
        self.root.title("Panneau d'Administration")
        self.root.geometry("1050x700")
        self.root.configure(bg=COLORS['bg'])
        
        self.ref_data = excel_mgr.load_reference_data()
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground=COLORS['text'],
                         rowheight=26, fieldbackground="white", font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=COLORS['primary'], foreground="white",
                         font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[('active', COLORS['primary_dark'])])
        style.map("Treeview", background=[('selected', '#1976D2')], foreground=[('selected', 'white')])
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=COLORS['header_bg'], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Panneau d'Administration",
                 font=("Segoe UI", 15, "bold"), bg=COLORS['header_bg'], fg="white").pack(pady=10)
        
        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=8)
        
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
        
        # Bottom buttons
        btn_frame = tk.Frame(self.root, bg=COLORS['bg'])
        btn_frame.pack(pady=8)
        btn_opts = {"font": ("Segoe UI", 11, "bold"), "fg": "white", "relief": "flat",
                    "cursor": "hand2", "width": 20}
        tk.Button(btn_frame, text="Sauvegarder les modifications", bg=COLORS['success'],
                  command=self.save_changes, **btn_opts).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Fermer", bg=COLORS['danger'],
                  command=self.root.destroy, **btn_opts).pack(side="left", padx=5)
    
    # ---- Helper: create a tab with search + tree ----
    def _make_tab(self, notebook, title, columns, data_key, data_list, add_cmd, format_row):
        """Generic tab with search bar and treeview"""
        frame = tk.Frame(notebook, bg=COLORS['card_bg'])
        notebook.add(frame, text=title)
        
        toolbar = tk.Frame(frame, bg=COLORS['toolbar_bg'])
        toolbar.pack(fill="x", padx=5, pady=4)
        
        btn_opts = {"font": ("Segoe UI", 9), "relief": "flat", "cursor": "hand2"}
        tk.Button(toolbar, text="+ Ajouter", bg=COLORS['success'], fg="white",
                  command=add_cmd, **btn_opts).pack(side="left", padx=3)
        
        tree_ref = [None]  # mutable to store reference
        tk.Button(toolbar, text="Supprimer", bg=COLORS['danger'], fg="white",
                  command=lambda: self.delete_selected(tree_ref[0], data_key),
                  **btn_opts).pack(side="left", padx=3)
        
        # Search
        tk.Label(toolbar, text="Rechercher :", font=("Segoe UI", 9),
                 bg=COLORS['toolbar_bg']).pack(side="left", padx=(15, 4))
        search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar, textvariable=search_var, width=20,
                                font=("Segoe UI", 9), relief="solid", bd=1)
        search_entry.pack(side="left", padx=3)
        
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        tree_ref[0] = tree
        
        # Populate
        for item in data_list:
            tree.insert('', 'end', values=format_row(item))
        
        # Search binding
        def do_search(*args):
            query = search_var.get().strip().lower()
            for child in tree.get_children():
                tree.delete(child)
            for item in self.ref_data.get(data_key, []):
                row_text = ' '.join(str(v) for v in format_row(item)).lower()
                if not query or query in row_text:
                    tree.insert('', 'end', values=format_row(item))
        
        search_var.trace_add("write", do_search)
        
        return tree
    
    # ---- Tabs ----
    def create_familles_tab(self, nb):
        self.familles_tree = self._make_tab(
            nb, "Familles", ('ID', 'Famille'), 'familles',
            self.ref_data.get('familles', []), self.add_famille,
            lambda f: (f['id'], f['famille']))
    
    def create_produits_tab(self, nb):
        self.produits_tree = self._make_tab(
            nb, "Produits", ('ID', 'ID Famille', 'Produit'), 'produits',
            self.ref_data.get('produits', []), self.add_produit,
            lambda p: (p['id'], p['famille_id'], p['produit']))
    
    def create_models_tab(self, nb):
        self.models_tree = self._make_tab(
            nb, "Modèles", ('ID', 'ID Produit', 'Modèle'), 'models',
            self.ref_data.get('models', []), self.add_model,
            lambda m: (m['id'], m['produit_id'], m['model']))
    
    def create_pannes_tab(self, nb):
        self.pannes_tree = self._make_tab(
            nb, "Pannes", ('ID', 'Code', 'ID Produit', 'Panne'), 'pannes',
            self.ref_data.get('pannes', []), self.add_panne,
            lambda p: (p['id'], p['code'], p['produit_id'], p['panne']))
    
    def create_causes_tab(self, nb):
        self.causes_tree = self._make_tab(
            nb, "Causes", ('ID', 'Code', 'ID Panne', 'Cause'), 'causes',
            self.ref_data.get('causes', []), self.add_cause,
            lambda c: (c['id'], c['code'], c['panne_id'], c['cause']))
    
    def create_solutions_tab(self, nb):
        self.solutions_tree = self._make_tab(
            nb, "Solutions", ('ID', 'Code', 'ID Cause', 'Solution'), 'solutions',
            self.ref_data.get('solutions', []), self.add_solution,
            lambda s: (s['id'], s['code'], s['cause_id'], s['solution']))
    
    def create_centres_tab(self, nb):
        self.centres_tree = self._make_tab(
            nb, "Centres", ('ID', 'Centre'), 'centres',
            self.ref_data.get('centres', []), self.add_centre,
            lambda c: (c['id'], c['centre']))
    
    # ---- Agents Agréés Tab (custom) ----
    def create_agents_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['card_bg'])
        notebook.add(frame, text="Agents Agréés")
        
        toolbar = tk.Frame(frame, bg=COLORS['toolbar_bg'])
        toolbar.pack(fill="x", padx=5, pady=4)
        
        btn_opts = {"font": ("Segoe UI", 9), "relief": "flat", "cursor": "hand2"}
        tk.Button(toolbar, text="+ Ajouter Agent", bg=COLORS['success'], fg="white",
                  command=self.add_agent, **btn_opts).pack(side="left", padx=3)
        tk.Button(toolbar, text="Importer Agents (Excel)", bg=COLORS['warning'], fg="white",
                  command=self.import_agents_excel, **btn_opts).pack(side="left", padx=3)
        tk.Button(toolbar, text="Supprimer", bg=COLORS['danger'], fg="white",
                  command=lambda: self.delete_selected(self.agents_tree, 'agents'),
                  **btn_opts).pack(side="left", padx=3)
        
        # Search
        tk.Label(toolbar, text="Rechercher :", font=("Segoe UI", 9),
                 bg=COLORS['toolbar_bg']).pack(side="left", padx=(15, 4))
        self.agent_search_var = tk.StringVar()
        tk.Entry(toolbar, textvariable=self.agent_search_var, width=20,
                 font=("Segoe UI", 9), relief="solid", bd=1).pack(side="left", padx=3)
        self.agent_search_var.trace_add("write", lambda *a: self._filter_agents())
        
        # Inline form
        form = tk.LabelFrame(frame, text="  Ajouter un nouvel Agent Agréé  ",
                              font=("Segoe UI", 9, "bold"), bg=COLORS['card_bg'],
                              fg=COLORS['primary'], padx=10, pady=5)
        form.pack(fill="x", padx=5, pady=4)
        
        lbl_opts = {"font": ("Segoe UI", 9), "bg": COLORS['card_bg']}
        tk.Label(form, text="Nom et Prénom :", **lbl_opts).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.agent_nom_entry = tk.Entry(form, width=25, font=("Segoe UI", 9), relief="solid", bd=1)
        self.agent_nom_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(form, text="Téléphone :", **lbl_opts).grid(row=0, column=2, sticky="e", padx=5, pady=2)
        self.agent_tel_entry = tk.Entry(form, width=18, font=("Segoe UI", 9), relief="solid", bd=1)
        self.agent_tel_entry.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(form, text="Wilaya :", **lbl_opts).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.agent_wilaya_entry = tk.Entry(form, width=25, font=("Segoe UI", 9), relief="solid", bd=1)
        self.agent_wilaya_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(form, text="Adresse :", **lbl_opts).grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.agent_adresse_entry = tk.Entry(form, width=18, font=("Segoe UI", 9), relief="solid", bd=1)
        self.agent_adresse_entry.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(form, text="+ Ajouter", bg=COLORS['success'], fg="white",
                  font=("Segoe UI", 9), relief="flat", cursor="hand2",
                  command=self.add_agent_from_form).grid(row=0, column=4, rowspan=2, padx=10, pady=2)
        
        # Tree
        self.agents_tree = ttk.Treeview(
            frame, columns=('ID', 'Nom Prénom', 'Téléphone', 'Wilaya', 'Adresse'),
            show='headings')
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
                a['id'], a['nom_prenom'], a['telephone'], a['wilaya'], a['adresse']))
    
    def _filter_agents(self):
        query = self.agent_search_var.get().strip().lower()
        for child in self.agents_tree.get_children():
            self.agents_tree.delete(child)
        for a in self.ref_data.get('agents', []):
            row = f"{a['id']} {a['nom_prenom']} {a['telephone']} {a['wilaya']} {a['adresse']}".lower()
            if not query or query in row:
                self.agents_tree.insert('', 'end', values=(
                    a['id'], a['nom_prenom'], a['telephone'], a['wilaya'], a['adresse']))
    
    # ---- Users Tab ----
    def create_users_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['card_bg'])
        notebook.add(frame, text="Utilisateurs")
        
        toolbar = tk.Frame(frame, bg=COLORS['toolbar_bg'])
        toolbar.pack(fill="x", padx=5, pady=4)
        
        btn_opts = {"font": ("Segoe UI", 9), "relief": "flat", "cursor": "hand2"}
        tk.Button(toolbar, text="+ Ajouter Utilisateur", bg=COLORS['success'], fg="white",
                  command=self.add_user, **btn_opts).pack(side="left", padx=3)
        tk.Button(toolbar, text="Réinitialiser Mot de passe", bg=COLORS['warning'], fg="white",
                  command=self.reset_password, **btn_opts).pack(side="left", padx=3)
        tk.Button(toolbar, text="Supprimer", bg=COLORS['danger'], fg="white",
                  command=lambda: self.delete_selected(self.users_tree, 'users'),
                  **btn_opts).pack(side="left", padx=3)
        
        self.users_tree = ttk.Treeview(frame, columns=('ID', 'Nom d\'utilisateur', 'Rôle'), show='headings')
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Nom d\'utilisateur', text="Nom d'utilisateur")
        self.users_tree.heading('Rôle', text='Rôle')
        self.users_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        for u in self.ref_data.get('users', []):
            self.users_tree.insert('', 'end', values=(u['id'], u['username'], u['role']))
    
    # ---- Import Data Tab ----
    def create_import_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['card_bg'])
        notebook.add(frame, text="Importer Données")
        
        # Reference data
        info = tk.LabelFrame(frame, text="  Importer les données de référence depuis Excel  ",
                              font=("Segoe UI", 10, "bold"), bg=COLORS['card_bg'],
                              fg=COLORS['primary'], padx=15, pady=10)
        info.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info, text=(
            "Importez des données depuis un fichier Excel avec la structure correspondante.\n"
            "Le fichier peut contenir ces feuilles :\n"
            "  Familles | Produits | Modèles | Pannes | Causes | Solutions\n"
            "  PDR | Centres | Agents\n\n"
            "Les données seront fusionnées avec les données existantes."
        ), font=("Segoe UI", 10), justify="left", bg=COLORS['card_bg']).pack(anchor="w")
        
        tk.Button(info, text="Sélectionner un fichier Excel et importer",
                  font=("Segoe UI", 11, "bold"), bg=COLORS['primary'], fg="white",
                  relief="flat", cursor="hand2",
                  command=self.import_reference_excel).pack(pady=10)
        
        # Agents import
        ag = tk.LabelFrame(frame, text="  Importer les Agents Agréés depuis Excel  ",
                            font=("Segoe UI", 10, "bold"), bg=COLORS['card_bg'],
                            fg=COLORS['primary'], padx=15, pady=10)
        ag.pack(fill="x", padx=10, pady=10)
        
        tk.Label(ag, text=(
            "Importez les agents depuis un fichier Excel avec les colonnes :\n"
            "  Nom_Prenom | Telephone | Wilaya | Adresse\n"
            "(La première ligne doit être l'en-tête)"
        ), font=("Segoe UI", 10), justify="left", bg=COLORS['card_bg']).pack(anchor="w")
        
        tk.Button(ag, text="Sélectionner un fichier Excel et importer les agents",
                  font=("Segoe UI", 11, "bold"), bg=COLORS['warning'], fg="white",
                  relief="flat", cursor="hand2",
                  command=self.import_agents_excel).pack(pady=10)
        
        # Log
        self.import_status = tk.Text(frame, height=6, state="disabled",
                                      font=("Consolas", 9), bg="#FAFAFA")
        self.import_status.pack(fill="both", expand=True, padx=10, pady=5)
    
    # ---- Archives Tab ----
    def create_archives_tab(self, notebook):
        frame = tk.Frame(notebook, bg=COLORS['card_bg'])
        notebook.add(frame, text="Archives")
        
        toolbar = tk.Frame(frame, bg=COLORS['toolbar_bg'])
        toolbar.pack(fill="x", padx=5, pady=4)
        
        btn_opts = {"font": ("Segoe UI", 9), "relief": "flat", "cursor": "hand2"}
        tk.Button(toolbar, text="Importer un rapport dans les archives",
                  bg=COLORS['primary'], fg="white", command=self.import_archive,
                  **btn_opts).pack(side="left", padx=5)
        tk.Button(toolbar, text="Actualiser", command=self.refresh_archives,
                  **btn_opts).pack(side="left", padx=5)
        tk.Button(toolbar, text="Voir le rapport sélectionné", command=self.view_archive,
                  **btn_opts).pack(side="left", padx=5)
        
        self.archives_tree = ttk.Treeview(frame, columns=('Fichier', 'Date', 'Taille'), show='headings')
        self.archives_tree.heading('Fichier', text='Nom du fichier')
        self.archives_tree.heading('Date', text='Date')
        self.archives_tree.heading('Taille', text='Taille')
        self.archives_tree.column('Fichier', width=350)
        self.archives_tree.column('Date', width=150)
        self.archives_tree.column('Taille', width=100)
        self.archives_tree.pack(fill="x", padx=5, pady=5)
        
        tk.Label(frame, text="Aperçu de l'archive :", font=("Segoe UI", 10, "bold"),
                 anchor="w", bg=COLORS['card_bg']).pack(fill="x", padx=5)
        
        pf = tk.Frame(frame, bg=COLORS['card_bg'])
        pf.pack(fill="both", expand=True, padx=5, pady=5)
        sy = ttk.Scrollbar(pf); sy.pack(side="right", fill="y")
        sx = ttk.Scrollbar(pf, orient="horizontal"); sx.pack(side="bottom", fill="x")
        self.archive_preview_tree = ttk.Treeview(pf, yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.archive_preview_tree.pack(fill="both", expand=True)
        sy.config(command=self.archive_preview_tree.yview)
        sx.config(command=self.archive_preview_tree.xview)
        
        cols = ('#', 'Client', 'Produit', 'Type', 'N° série', 'Garantie',
                'Date prod.', 'Panne', 'Réparation', 'PDR', 'Statut',
                'Centre', 'Date réc.', 'Date rép.')
        self.archive_preview_tree['columns'] = cols
        self.archive_preview_tree['show'] = 'headings'
        for c in cols:
            self.archive_preview_tree.heading(c, text=c)
            self.archive_preview_tree.column(c, width=90)
        
        self.refresh_archives()
    
    # ============ CRUD ============
    
    def add_famille(self):
        name = simpledialog.askstring("Ajouter Famille", "Nom de la famille :")
        if name:
            new_id = max([f['id'] for f in self.ref_data['familles']], default=0) + 1
            self.ref_data['familles'].append({'id': new_id, 'famille': name})
            self.familles_tree.insert('', 'end', values=(new_id, name))
    
    def add_produit(self):
        fid = simpledialog.askinteger("Ajouter Produit", "ID de la famille :")
        if fid:
            name = simpledialog.askstring("Ajouter Produit", "Nom du produit :")
            if name:
                new_id = max([p['id'] for p in self.ref_data['produits']], default=0) + 1
                self.ref_data['produits'].append({'id': new_id, 'famille_id': fid, 'produit': name})
                self.produits_tree.insert('', 'end', values=(new_id, fid, name))
    
    def add_model(self):
        pid = simpledialog.askinteger("Ajouter Modèle", "ID du produit :")
        if pid:
            name = simpledialog.askstring("Ajouter Modèle", "Nom du modèle :")
            if name:
                new_id = max([m['id'] for m in self.ref_data['models']], default=0) + 1
                self.ref_data['models'].append({'id': new_id, 'produit_id': pid, 'model': name})
                self.models_tree.insert('', 'end', values=(new_id, pid, name))
    
    def add_panne(self):
        pid = simpledialog.askinteger("Ajouter Panne", "ID du produit :")
        if pid:
            code = simpledialog.askstring("Ajouter Panne", "Code de la panne :")
            if code:
                name = simpledialog.askstring("Ajouter Panne", "Nom de la panne :")
                if name:
                    new_id = max([p['id'] for p in self.ref_data['pannes']], default=0) + 1
                    self.ref_data['pannes'].append({'id': new_id, 'code': code, 'produit_id': pid, 'panne': name})
                    self.pannes_tree.insert('', 'end', values=(new_id, code, pid, name))
    
    def add_cause(self):
        pid = simpledialog.askinteger("Ajouter Cause", "ID de la panne :")
        if pid:
            code = simpledialog.askstring("Ajouter Cause", "Code de la cause :")
            if code:
                name = simpledialog.askstring("Ajouter Cause", "Nom de la cause :")
                if name:
                    new_id = max([c['id'] for c in self.ref_data['causes']], default=0) + 1
                    self.ref_data['causes'].append({'id': new_id, 'code': code, 'panne_id': pid, 'cause': name})
                    self.causes_tree.insert('', 'end', values=(new_id, code, pid, name))
    
    def add_solution(self):
        cid = simpledialog.askinteger("Ajouter Solution", "ID de la cause :")
        if cid:
            code = simpledialog.askstring("Ajouter Solution", "Code de la solution :")
            if code:
                name = simpledialog.askstring("Ajouter Solution", "Nom de la solution :")
                if name:
                    new_id = max([s['id'] for s in self.ref_data['solutions']], default=0) + 1
                    self.ref_data['solutions'].append({'id': new_id, 'code': code, 'cause_id': cid, 'solution': name})
                    self.solutions_tree.insert('', 'end', values=(new_id, code, cid, name))
    
    def add_centre(self):
        name = simpledialog.askstring("Ajouter Centre", "Nom du centre (ex. Centre BBA) :")
        if name:
            new_id = max([c['id'] for c in self.ref_data['centres']], default=0) + 1
            self.ref_data['centres'].append({'id': new_id, 'centre': name})
            self.centres_tree.insert('', 'end', values=(new_id, name))
    
    def add_agent(self):
        nom = simpledialog.askstring("Ajouter Agent Agréé", "Nom et Prénom :")
        if nom:
            tel = simpledialog.askstring("Ajouter Agent Agréé", "Téléphone :") or ''
            wilaya = simpledialog.askstring("Ajouter Agent Agréé", "Wilaya :") or ''
            adresse = simpledialog.askstring("Ajouter Agent Agréé", "Adresse :") or ''
            new_id = max([a['id'] for a in self.ref_data.get('agents', [])], default=0) + 1
            new_agent = {'id': new_id, 'nom_prenom': nom, 'telephone': tel, 'wilaya': wilaya, 'adresse': adresse}
            if 'agents' not in self.ref_data:
                self.ref_data['agents'] = []
            self.ref_data['agents'].append(new_agent)
            self.agents_tree.insert('', 'end', values=(new_id, nom, tel, wilaya, adresse))
    
    def add_agent_from_form(self):
        nom = self.agent_nom_entry.get().strip()
        if not nom:
            messagebox.showwarning("Attention", "Le champ Nom et Prénom est obligatoire")
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
        self.agent_nom_entry.delete(0, tk.END)
        self.agent_tel_entry.delete(0, tk.END)
        self.agent_wilaya_entry.delete(0, tk.END)
        self.agent_adresse_entry.delete(0, tk.END)
    
    def add_user(self):
        username = simpledialog.askstring("Ajouter Utilisateur", "Nom d'utilisateur :")
        if username:
            password = simpledialog.askstring("Ajouter Utilisateur", "Mot de passe :")
            if password:
                role = simpledialog.askstring("Ajouter Utilisateur", "Rôle (admin/inserter) :")
                if role in ['admin', 'inserter']:
                    new_id = max([u['id'] for u in self.ref_data['users']], default=0) + 1
                    self.ref_data['users'].append({'id': new_id, 'username': username, 'password': password, 'role': role})
                    self.users_tree.insert('', 'end', values=(new_id, username, role))
    
    def reset_password(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur")
            return
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        new_pw = simpledialog.askstring("Réinitialiser Mot de passe", "Nouveau mot de passe :")
        if new_pw:
            for user in self.ref_data['users']:
                if user['id'] == user_id:
                    user['password'] = new_pw
                    messagebox.showinfo("Succès", "Mot de passe réinitialisé avec succès")
                    break
    
    def delete_selected(self, tree, data_key):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à supprimer")
            return
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer cet élément ?"):
            item = tree.item(selection[0])
            item_id = item['values'][0]
            self.ref_data[data_key] = [x for x in self.ref_data[data_key] if x['id'] != item_id]
            tree.delete(selection[0])
    
    def save_changes(self):
        try:
            self.excel_mgr.save_reference_data(self.ref_data)
            messagebox.showinfo("Succès", "Modifications sauvegardées avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de la sauvegarde : {str(e)}")
    
    # ============ Import ============
    
    def _log_import(self, message):
        self.import_status.config(state="normal")
        self.import_status.insert(tk.END, message + "\n")
        self.import_status.see(tk.END)
        self.import_status.config(state="disabled")
    
    def import_reference_excel(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier Excel de données",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
        if not file_path:
            return
        self._log_import(f"Importation depuis : {file_path}")
        success, msg = self.excel_mgr.import_reference_from_excel(file_path)
        self._log_import(msg)
        if success:
            self.ref_data = self.excel_mgr.load_reference_data()
            self._refresh_all_trees()
            messagebox.showinfo("Importation réussie", msg)
        else:
            messagebox.showerror("Erreur d'importation", msg)
    
    def import_agents_excel(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier Excel des Agents Agréés",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
        if not file_path:
            return
        if hasattr(self, 'import_status'):
            self._log_import(f"Importation des agents depuis : {file_path}")
        success, msg = self.excel_mgr.import_agents_from_excel(file_path)
        if hasattr(self, 'import_status'):
            self._log_import(msg)
        if success:
            self.ref_data = self.excel_mgr.load_reference_data()
            self._refresh_agents_tree()
            messagebox.showinfo("Importation réussie", msg)
        else:
            messagebox.showerror("Erreur d'importation", msg)
    
    def _refresh_all_trees(self):
        for item in self.familles_tree.get_children(): self.familles_tree.delete(item)
        for f in self.ref_data.get('familles', []):
            self.familles_tree.insert('', 'end', values=(f['id'], f['famille']))
        
        for item in self.produits_tree.get_children(): self.produits_tree.delete(item)
        for p in self.ref_data.get('produits', []):
            self.produits_tree.insert('', 'end', values=(p['id'], p['famille_id'], p['produit']))
        
        for item in self.models_tree.get_children(): self.models_tree.delete(item)
        for m in self.ref_data.get('models', []):
            self.models_tree.insert('', 'end', values=(m['id'], m['produit_id'], m['model']))
        
        for item in self.pannes_tree.get_children(): self.pannes_tree.delete(item)
        for p in self.ref_data.get('pannes', []):
            self.pannes_tree.insert('', 'end', values=(p['id'], p['code'], p['produit_id'], p['panne']))
        
        for item in self.causes_tree.get_children(): self.causes_tree.delete(item)
        for c in self.ref_data.get('causes', []):
            self.causes_tree.insert('', 'end', values=(c['id'], c['code'], c['panne_id'], c['cause']))
        
        for item in self.solutions_tree.get_children(): self.solutions_tree.delete(item)
        for s in self.ref_data.get('solutions', []):
            self.solutions_tree.insert('', 'end', values=(s['id'], s['code'], s['cause_id'], s['solution']))
        
        for item in self.centres_tree.get_children(): self.centres_tree.delete(item)
        for c in self.ref_data.get('centres', []):
            self.centres_tree.insert('', 'end', values=(c['id'], c['centre']))
        
        self._refresh_agents_tree()
        
        for item in self.users_tree.get_children(): self.users_tree.delete(item)
        for u in self.ref_data.get('users', []):
            self.users_tree.insert('', 'end', values=(u['id'], u['username'], u['role']))
    
    def _refresh_agents_tree(self):
        for item in self.agents_tree.get_children(): self.agents_tree.delete(item)
        for a in self.ref_data.get('agents', []):
            self.agents_tree.insert('', 'end', values=(
                a['id'], a['nom_prenom'], a['telephone'], a['wilaya'], a['adresse']))
    
    # ============ Archives ============
    
    def refresh_archives(self):
        for item in self.archives_tree.get_children(): self.archives_tree.delete(item)
        for arc in self.excel_mgr.list_archives():
            size_kb = f"{arc['size'] / 1024:.1f} Ko"
            self.archives_tree.insert('', 'end', values=(arc['filename'], arc['date'], size_kb))
    
    def import_archive(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner le rapport mensuel à archiver",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
        if not file_path:
            return
        success, msg = self.excel_mgr.import_archive(file_path)
        if success:
            self.refresh_archives()
            messagebox.showinfo("Archivage réussi", msg)
        else:
            messagebox.showerror("Erreur d'archivage", msg)
    
    def view_archive(self):
        selection = self.archives_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une archive")
            return
        item = self.archives_tree.item(selection[0])
        filename = item['values'][0]
        archive_path = os.path.join(self.excel_mgr.archives_dir, filename)
        for child in self.archive_preview_tree.get_children():
            self.archive_preview_tree.delete(child)
        insertions = self.excel_mgr.load_archive_data(archive_path)
        if not insertions:
            messagebox.showinfo("Info", "Aucune donnée trouvée dans cette archive")
            return
        for ins in insertions:
            self.archive_preview_tree.insert('', 'end', values=(
                ins.get('num', ''), ins.get('client', ''), ins.get('produit', ''),
                ins.get('type_produit', ''), ins.get('num_serie', ''), ins.get('garantie', ''),
                ins.get('date_produit', ''), ins.get('panne', ''), ins.get('reparation', ''),
                ins.get('pdr', ''), ins.get('statut', ''), ins.get('centre', ''),
                ins.get('date_reception', ''), ins.get('date_reparation', '')))
