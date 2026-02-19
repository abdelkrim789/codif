"""Tableau de bord principal avec filtres de recherche"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.excel_manager import ExcelManager
from app.gui.insertion import InsertionWindow
from app.gui.admin_panel import AdminPanel
from app.gui.report import ReportGenerator


# Modern color palette
COLORS = {
    'primary': '#1565C0',
    'primary_dark': '#0D47A1',
    'primary_light': '#1976D2',
    'accent': '#00897B',
    'success': '#2E7D32',
    'danger': '#C62828',
    'warning': '#EF6C00',
    'bg': '#ECEFF1',
    'card_bg': '#FFFFFF',
    'text': '#212121',
    'text_light': '#757575',
    'border': '#CFD8DC',
    'header_bg': '#1565C0',
    'toolbar_bg': '#FAFAFA',
    'filter_bg': '#E3F2FD',
    'row_alt': '#F5F5F5',
    'row_hover': '#E8EAF6',
}


class Dashboard:
    """Fenêtre du tableau de bord principal"""
    
    def __init__(self, root, auth_mgr):
        self.root = root
        self.auth_mgr = auth_mgr
        self.excel_mgr = ExcelManager()
        self.all_insertions = []  # Cache for filtering
        
        self.root.title("Gestion SAV - Tableau de Bord")
        self.root.geometry("1300x750")
        self.root.configure(bg=COLORS['bg'])
        
        self.center_window()
        self.setup_styles()
        self.create_widgets()
        self.load_data()
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = 1300, 750
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                         background="white",
                         foreground=COLORS['text'],
                         rowheight=28,
                         fieldbackground="white",
                         font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                         background=COLORS['primary'],
                         foreground="white",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat")
        style.map("Treeview.Heading",
                   background=[('active', COLORS['primary_dark'])])
        style.map("Treeview",
                   background=[('selected', COLORS['primary_light'])],
                   foreground=[('selected', 'white')])
        
        style.configure("Filter.TCombobox", padding=4)
    
    def create_widgets(self):
        """Créer les widgets du tableau de bord"""
        # ===== Header =====
        header = tk.Frame(self.root, bg=COLORS['header_bg'], height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Gestion SAV — Tableau de Bord",
                 font=("Segoe UI", 16, "bold"),
                 bg=COLORS['header_bg'], fg="white").pack(side="left", padx=20, pady=12)
        
        user = self.auth_mgr.get_current_user()
        tk.Label(header,
                 text=f"Utilisateur : {user['username']} ({user['role'].upper()})",
                 font=("Segoe UI", 10), bg=COLORS['header_bg'], fg="#BBDEFB"
                 ).pack(side="right", padx=20, pady=12)
        
        logout_btn = tk.Button(header, text="Déconnexion",
                               font=("Segoe UI", 9), bg=COLORS['danger'], fg="white",
                               relief="flat", cursor="hand2", command=self.logout)
        logout_btn.pack(side="right", padx=5, pady=12)
        
        # ===== Toolbar =====
        toolbar = tk.Frame(self.root, bg=COLORS['toolbar_bg'], height=50)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)
        
        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white",
                     "relief": "flat", "cursor": "hand2", "padx": 12}
        
        tk.Button(toolbar, text="＋ Nouvelle Insertion", bg=COLORS['success'],
                  command=self.open_insertion_form, **btn_style).pack(side="left", padx=8, pady=8)
        tk.Button(toolbar, text="⟳ Actualiser", bg=COLORS['primary'],
                  command=self.load_data, **btn_style).pack(side="left", padx=4, pady=8)
        tk.Button(toolbar, text="Exporter Rapport", bg=COLORS['warning'],
                  command=self.export_report, **btn_style).pack(side="left", padx=4, pady=8)
        
        if self.auth_mgr.is_admin():
            tk.Button(toolbar, text="Administration", bg="#6A1B9A",
                      command=self.open_admin_panel, **btn_style).pack(side="left", padx=4, pady=8)
            tk.Button(toolbar, text="Archives", bg="#455A64",
                      command=self.open_archives, **btn_style).pack(side="left", padx=4, pady=8)
        
        # ===== Filter Section =====
        filter_frame = tk.LabelFrame(self.root, text="  Recherche et Filtres  ",
                                      font=("Segoe UI", 10, "bold"),
                                      bg=COLORS['filter_bg'], fg=COLORS['primary_dark'],
                                      bd=1, relief="solid")
        filter_frame.pack(fill="x", padx=10, pady=(8, 4))
        
        inner = tk.Frame(filter_frame, bg=COLORS['filter_bg'])
        inner.pack(fill="x", padx=10, pady=8)
        
        lbl_opts = {"font": ("Segoe UI", 9), "bg": COLORS['filter_bg'], "fg": COLORS['text']}
        entry_opts = {"font": ("Segoe UI", 9), "relief": "solid", "bd": 1}
        
        # Row 1: text searches
        tk.Label(inner, text="Recherche globale :", **lbl_opts).grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.apply_filters())
        search_entry = tk.Entry(inner, textvariable=self.search_var, width=25, **entry_opts)
        search_entry.grid(row=0, column=1, padx=4, pady=3)
        
        tk.Label(inner, text="Client :", **lbl_opts).grid(row=0, column=2, sticky="e", padx=4, pady=3)
        self.filter_client_var = tk.StringVar()
        self.filter_client_var.trace_add("write", lambda *a: self.apply_filters())
        tk.Entry(inner, textvariable=self.filter_client_var, width=18, **entry_opts).grid(row=0, column=3, padx=4, pady=3)
        
        tk.Label(inner, text="N° Série :", **lbl_opts).grid(row=0, column=4, sticky="e", padx=4, pady=3)
        self.filter_serie_var = tk.StringVar()
        self.filter_serie_var.trace_add("write", lambda *a: self.apply_filters())
        tk.Entry(inner, textvariable=self.filter_serie_var, width=15, **entry_opts).grid(row=0, column=5, padx=4, pady=3)
        
        # Row 2: dropdowns
        tk.Label(inner, text="Produit :", **lbl_opts).grid(row=1, column=0, sticky="e", padx=4, pady=3)
        self.filter_produit_var = tk.StringVar()
        self.filter_produit_combo = ttk.Combobox(inner, textvariable=self.filter_produit_var,
                                                  state="readonly", width=22)
        self.filter_produit_combo.grid(row=1, column=1, padx=4, pady=3)
        self.filter_produit_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        tk.Label(inner, text="Statut :", **lbl_opts).grid(row=1, column=2, sticky="e", padx=4, pady=3)
        self.filter_statut_var = tk.StringVar()
        self.filter_statut_combo = ttk.Combobox(inner, textvariable=self.filter_statut_var,
                                                 state="readonly", width=15,
                                                 values=["", "Réparé", "En cours", "Non réparé",
                                                         "Pièce non disponible", "Changé"])
        self.filter_statut_combo.grid(row=1, column=3, padx=4, pady=3)
        self.filter_statut_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        tk.Label(inner, text="Centre :", **lbl_opts).grid(row=1, column=4, sticky="e", padx=4, pady=3)
        self.filter_centre_var = tk.StringVar()
        self.filter_centre_combo = ttk.Combobox(inner, textvariable=self.filter_centre_var,
                                                 state="readonly", width=15)
        self.filter_centre_combo.grid(row=1, column=5, padx=4, pady=3)
        self.filter_centre_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Row 3: date range + garantie + reset
        tk.Label(inner, text="Garantie :", **lbl_opts).grid(row=2, column=0, sticky="e", padx=4, pady=3)
        self.filter_garantie_var = tk.StringVar()
        self.filter_garantie_combo = ttk.Combobox(inner, textvariable=self.filter_garantie_var,
                                                   state="readonly", width=22,
                                                   values=["", "Garantie", "Hors Garantie",
                                                           "Fiche de garantie", "Non-conforme"])
        self.filter_garantie_combo.grid(row=2, column=1, padx=4, pady=3)
        self.filter_garantie_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        tk.Label(inner, text="Date réception du :", **lbl_opts).grid(row=2, column=2, sticky="e", padx=4, pady=3)
        self.filter_date_from_var = tk.StringVar()
        self.filter_date_from_var.trace_add("write", lambda *a: self.apply_filters())
        tk.Entry(inner, textvariable=self.filter_date_from_var, width=12, **entry_opts).grid(row=2, column=3, padx=4, pady=3, sticky="w")
        
        tk.Label(inner, text="au :", **lbl_opts).grid(row=2, column=4, sticky="e", padx=4, pady=3)
        self.filter_date_to_var = tk.StringVar()
        self.filter_date_to_var.trace_add("write", lambda *a: self.apply_filters())
        tk.Entry(inner, textvariable=self.filter_date_to_var, width=12, **entry_opts).grid(row=2, column=5, padx=4, pady=3, sticky="w")
        
        reset_btn = tk.Button(inner, text="✕ Réinitialiser", font=("Segoe UI", 9),
                              bg=COLORS['danger'], fg="white", relief="flat", cursor="hand2",
                              command=self.reset_filters)
        reset_btn.grid(row=2, column=6, padx=8, pady=3)
        
        # ===== Table =====
        table_frame = tk.Frame(self.root, bg=COLORS['bg'])
        table_frame.pack(fill="both", expand=True, padx=10, pady=(4, 8))
        
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(table_frame,
                                  yscrollcommand=tree_scroll_y.set,
                                  xscrollcommand=tree_scroll_x.set)
        self.tree.pack(fill="both", expand=True)
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        columns = ('#', 'Client', 'Produit', 'Type de produit', 'N° de série',
                   'Garantie', 'Date produit', 'Panne', 'Réparation effectuée',
                   'PDR consommée', 'Statut', 'Centre', 'Date réception', 'Date réparation')
        
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            if col == '#':
                self.tree.column(col, width=40, anchor='center')
            elif col in ('Client', 'N° de série'):
                self.tree.column(col, width=110)
            elif col in ('Produit', 'Type de produit', 'Panne', 'Réparation effectuée', 'PDR consommée'):
                self.tree.column(col, width=140)
            else:
                self.tree.column(col, width=100)
        
        # Alternating row colors
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background=COLORS['row_alt'])
        
        # ===== Status bar =====
        status_frame = tk.Frame(self.root, bg=COLORS['primary_dark'], height=28)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Prêt",
                                      font=("Segoe UI", 9), bg=COLORS['primary_dark'],
                                      fg="white", anchor="w")
        self.status_label.pack(side="left", padx=10)
        
        self.count_label = tk.Label(status_frame, text="",
                                     font=("Segoe UI", 9), bg=COLORS['primary_dark'],
                                     fg="#BBDEFB", anchor="e")
        self.count_label.pack(side="right", padx=10)
        
        # Sort state
        self.sort_col = None
        self.sort_reverse = False
    
    def load_data(self):
        """Charger les données d'insertion dans le tableau"""
        self.all_insertions = self.excel_mgr.load_insertions()
        self._populate_filter_combos()
        self.apply_filters()
        self.status_label.config(text=f"{len(self.all_insertions)} insertion(s) chargée(s)")
    
    def _populate_filter_combos(self):
        """Populate filter dropdowns from loaded data"""
        produits = sorted(set(str(i.get('produit', '')) for i in self.all_insertions if i.get('produit')))
        centres = sorted(set(str(i.get('centre', '')) for i in self.all_insertions if i.get('centre')))
        self.filter_produit_combo['values'] = [""] + produits
        self.filter_centre_combo['values'] = [""] + centres
    
    def apply_filters(self):
        """Apply all filters and update the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search = self.search_var.get().strip().lower()
        f_client = self.filter_client_var.get().strip().lower()
        f_serie = self.filter_serie_var.get().strip().lower()
        f_produit = self.filter_produit_var.get().strip()
        f_statut = self.filter_statut_var.get().strip()
        f_centre = self.filter_centre_var.get().strip()
        f_garantie = self.filter_garantie_var.get().strip()
        f_date_from = self.filter_date_from_var.get().strip()
        f_date_to = self.filter_date_to_var.get().strip()
        
        filtered = []
        for ins in self.all_insertions:
            # Global search
            if search:
                row_text = ' '.join(str(v) for v in ins.values()).lower()
                if search not in row_text:
                    continue
            # Client filter
            if f_client and f_client not in str(ins.get('client', '')).lower():
                continue
            # Serial number filter
            if f_serie and f_serie not in str(ins.get('num_serie', '')).lower():
                continue
            # Produit filter
            if f_produit and str(ins.get('produit', '')) != f_produit:
                continue
            # Statut filter
            if f_statut and str(ins.get('statut', '')) != f_statut:
                continue
            # Centre filter
            if f_centre and str(ins.get('centre', '')) != f_centre:
                continue
            # Garantie filter
            if f_garantie and str(ins.get('garantie', '')) != f_garantie:
                continue
            # Date range filter
            date_rec = str(ins.get('date_reception', ''))
            if f_date_from and date_rec < f_date_from:
                continue
            if f_date_to and date_rec > f_date_to:
                continue
            
            filtered.append(ins)
        
        for idx, ins in enumerate(filtered):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                ins.get('num', ''), ins.get('client', ''), ins.get('produit', ''),
                ins.get('type_produit', ''), ins.get('num_serie', ''),
                ins.get('garantie', ''), ins.get('date_produit', ''),
                ins.get('panne', ''), ins.get('reparation', ''),
                ins.get('pdr', ''), ins.get('statut', ''),
                ins.get('centre', ''), ins.get('date_reception', ''),
                ins.get('date_reparation', '')
            ), tags=(tag,))
        
        self.count_label.config(
            text=f"Affichage : {len(filtered)} / {len(self.all_insertions)} insertion(s)")
    
    def reset_filters(self):
        """Réinitialiser tous les filtres"""
        self.search_var.set('')
        self.filter_client_var.set('')
        self.filter_serie_var.set('')
        self.filter_produit_var.set('')
        self.filter_statut_var.set('')
        self.filter_centre_var.set('')
        self.filter_garantie_var.set('')
        self.filter_date_from_var.set('')
        self.filter_date_to_var.set('')
    
    def sort_column(self, col):
        """Sort table by clicking on column header"""
        if self.sort_col == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_col = col
            self.sort_reverse = False
        
        columns = self.tree['columns']
        col_index = list(columns).index(col)
        
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(key=lambda t: str(t[0]).lower(), reverse=self.sort_reverse)
        
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.item(k, tags=(tag,))
    
    def open_insertion_form(self):
        insertion_window = tk.Toplevel(self.root)
        InsertionWindow(insertion_window, self.excel_mgr, self.on_insertion_added)
    
    def on_insertion_added(self):
        self.load_data()
        messagebox.showinfo("Succès", "Insertion ajoutée avec succès !")
    
    def open_admin_panel(self):
        admin_window = tk.Toplevel(self.root)
        AdminPanel(admin_window, self.excel_mgr)
    
    def open_archives(self):
        from app.gui.archives import ArchivesWindow
        archives_window = tk.Toplevel(self.root)
        ArchivesWindow(archives_window, self.excel_mgr)
    
    def export_report(self):
        report_gen = ReportGenerator(self.excel_mgr)
        success, message = report_gen.generate_report()
        if success:
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showerror("Erreur", message)
    
    def logout(self):
        if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
            self.auth_mgr.logout()
            self.root.destroy()
