"""Archives viewer window for browsing previous monthly reports"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ArchivesWindow:
    """Window for managing and viewing archived monthly reports"""
    
    def __init__(self, root, excel_mgr):
        self.root = root
        self.excel_mgr = excel_mgr
        
        self.root.title("Archives - Previous Monthly Reports")
        self.root.geometry("1100x600")
        
        self.create_widgets()
        self.refresh_archives()
    
    def create_widgets(self):
        # Toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", padx=10, pady=5)
        
        tk.Button(toolbar, text="Import Report to Archive", bg="#2196F3", fg="white",
                  font=("Arial", 10), command=self.import_archive).pack(side="left", padx=5)
        tk.Button(toolbar, text="Refresh", font=("Arial", 10),
                  command=self.refresh_archives).pack(side="left", padx=5)
        tk.Button(toolbar, text="View Selected", font=("Arial", 10),
                  command=self.view_archive).pack(side="left", padx=5)
        
        # Archives list
        list_frame = tk.LabelFrame(self.root, text="Archived Reports")
        list_frame.pack(fill="x", padx=10, pady=5)
        
        self.archives_tree = ttk.Treeview(list_frame, columns=('Filename', 'Date', 'Size'),
                                          show='headings', height=6)
        self.archives_tree.heading('Filename', text='Filename')
        self.archives_tree.heading('Date', text='Date')
        self.archives_tree.heading('Size', text='Size')
        self.archives_tree.column('Filename', width=400)
        self.archives_tree.column('Date', width=180)
        self.archives_tree.column('Size', width=100)
        self.archives_tree.pack(fill="x", padx=5, pady=5)
        
        # Preview
        preview_label = tk.Label(self.root, text="Report Preview:", font=("Arial", 10, "bold"), anchor="w")
        preview_label.pack(fill="x", padx=10)
        
        preview_frame = tk.Frame(self.root)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scroll_y = ttk.Scrollbar(preview_frame)
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(preview_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.preview_tree = ttk.Treeview(
            preview_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.preview_tree.pack(fill="both", expand=True)
        scroll_y.config(command=self.preview_tree.yview)
        scroll_x.config(command=self.preview_tree.xview)
        
        columns = ('#', 'Client', 'Produit', 'Type', 'N° série', 'Garantie',
                   'Date prod.', 'Panne', 'Réparation', 'PDR', 'Statut',
                   'Centre', 'Date réc.', 'Date rép.')
        self.preview_tree['columns'] = columns
        self.preview_tree['show'] = 'headings'
        for col in columns:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=90)
    
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
        
        for child in self.preview_tree.get_children():
            self.preview_tree.delete(child)
        
        insertions = self.excel_mgr.load_archive_data(archive_path)
        if not insertions:
            messagebox.showinfo("Info", "No data found in this archive")
            return
        
        for ins in insertions:
            self.preview_tree.insert('', 'end', values=(
                ins.get('num', ''), ins.get('client', ''), ins.get('produit', ''),
                ins.get('type_produit', ''), ins.get('num_serie', ''), ins.get('garantie', ''),
                ins.get('date_produit', ''), ins.get('panne', ''), ins.get('reparation', ''),
                ins.get('pdr', ''), ins.get('statut', ''), ins.get('centre', ''),
                ins.get('date_reception', ''), ins.get('date_reparation', '')
            ))
