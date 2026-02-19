"""Fenêtre de consultation des archives des rapports mensuels"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


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
    'toolbar_bg': '#FAFAFA',
}


class ArchivesWindow:
    """Fenêtre de gestion et de consultation des rapports mensuels archivés"""
    
    def __init__(self, root, excel_mgr):
        self.root = root
        self.excel_mgr = excel_mgr
        
        self.root.title("Archives — Rapports Mensuels")
        self.root.geometry("1100x620")
        self.root.configure(bg=COLORS['bg'])
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_archives()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground=COLORS['text'],
                         rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=COLORS['primary'], foreground="white",
                         font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[('active', COLORS['primary_dark'])])
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=COLORS['header_bg'], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Archives — Rapports Mensuels",
                 font=("Segoe UI", 14, "bold"), bg=COLORS['header_bg'], fg="white").pack(pady=8)
        
        # Toolbar
        toolbar = tk.Frame(self.root, bg=COLORS['toolbar_bg'])
        toolbar.pack(fill="x", padx=10, pady=5)
        
        btn_opts = {"font": ("Segoe UI", 10), "fg": "white", "relief": "flat", "cursor": "hand2"}
        tk.Button(toolbar, text="Importer un rapport", bg=COLORS['primary'],
                  command=self.import_archive, **btn_opts).pack(side="left", padx=5)
        tk.Button(toolbar, text="Actualiser", bg="#455A64",
                  command=self.refresh_archives, **btn_opts).pack(side="left", padx=5)
        tk.Button(toolbar, text="Voir le rapport sélectionné", bg=COLORS['success'],
                  command=self.view_archive, **btn_opts).pack(side="left", padx=5)
        
        # Archives list
        list_frame = tk.LabelFrame(self.root, text="  Rapports archivés  ",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=COLORS['card_bg'], fg=COLORS['primary'])
        list_frame.pack(fill="x", padx=10, pady=5)
        
        self.archives_tree = ttk.Treeview(list_frame,
                                           columns=('Fichier', 'Date', 'Taille'),
                                           show='headings', height=5)
        self.archives_tree.heading('Fichier', text='Nom du fichier')
        self.archives_tree.heading('Date', text='Date')
        self.archives_tree.heading('Taille', text='Taille')
        self.archives_tree.column('Fichier', width=400)
        self.archives_tree.column('Date', width=180)
        self.archives_tree.column('Taille', width=100)
        self.archives_tree.pack(fill="x", padx=5, pady=5)
        
        # Preview
        tk.Label(self.root, text="Aperçu du rapport :", font=("Segoe UI", 10, "bold"),
                 anchor="w", bg=COLORS['bg']).pack(fill="x", padx=10)
        
        pf = tk.Frame(self.root)
        pf.pack(fill="both", expand=True, padx=10, pady=5)
        sy = ttk.Scrollbar(pf); sy.pack(side="right", fill="y")
        sx = ttk.Scrollbar(pf, orient="horizontal"); sx.pack(side="bottom", fill="x")
        self.preview_tree = ttk.Treeview(pf, yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.preview_tree.pack(fill="both", expand=True)
        sy.config(command=self.preview_tree.yview)
        sx.config(command=self.preview_tree.xview)
        
        cols = ('#', 'Client', 'Produit', 'Type', 'N° série', 'Garantie',
                'Date prod.', 'Panne', 'Réparation', 'PDR', 'Statut',
                'Centre', 'Date réc.', 'Date rép.')
        self.preview_tree['columns'] = cols
        self.preview_tree['show'] = 'headings'
        for c in cols:
            self.preview_tree.heading(c, text=c)
            self.preview_tree.column(c, width=90)
    
    def refresh_archives(self):
        for item in self.archives_tree.get_children():
            self.archives_tree.delete(item)
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
        for child in self.preview_tree.get_children():
            self.preview_tree.delete(child)
        insertions = self.excel_mgr.load_archive_data(archive_path)
        if not insertions:
            messagebox.showinfo("Info", "Aucune donnée trouvée dans cette archive")
            return
        for ins in insertions:
            self.preview_tree.insert('', 'end', values=(
                ins.get('num', ''), ins.get('client', ''), ins.get('produit', ''),
                ins.get('type_produit', ''), ins.get('num_serie', ''), ins.get('garantie', ''),
                ins.get('date_produit', ''), ins.get('panne', ''), ins.get('reparation', ''),
                ins.get('pdr', ''), ins.get('statut', ''), ins.get('centre', ''),
                ins.get('date_reception', ''), ins.get('date_reparation', '')))
