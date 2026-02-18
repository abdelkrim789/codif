"""Main dashboard window"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.excel_manager import ExcelManager
from app.gui.insertion import InsertionWindow
from app.gui.admin_panel import AdminPanel
from app.gui.report import ReportGenerator


class Dashboard:
    """Main dashboard window"""
    
    def __init__(self, root, auth_mgr):
        self.root = root
        self.auth_mgr = auth_mgr
        self.excel_mgr = ExcelManager()
        
        self.root.title("SAV Repair Data - Dashboard")
        self.root.geometry("1200x700")
        
        # Center the window
        self.center_window()
        
        self.create_widgets()
        self.load_data()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Top bar
        top_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            top_frame,
            text="SAV Repair Data Management System",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # User info
        user = self.auth_mgr.get_current_user()
        user_label = tk.Label(
            top_frame,
            text=f"User: {user['username']} ({user['role'].upper()})",
            font=("Arial", 11),
            bg="#2196F3",
            fg="white"
        )
        user_label.pack(side="right", padx=20, pady=15)
        
        # Logout button
        logout_btn = tk.Button(
            top_frame,
            text="Logout",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            command=self.logout
        )
        logout_btn.pack(side="right", padx=10, pady=15)
        
        # Button bar
        button_frame = tk.Frame(self.root, bg="#f0f0f0", height=50)
        button_frame.pack(fill="x")
        button_frame.pack_propagate(False)
        
        # New insertion button
        new_btn = tk.Button(
            button_frame,
            text="➕ New Insertion",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.open_insertion_form
        )
        new_btn.pack(side="left", padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.load_data
        )
        refresh_btn.pack(side="left", padx=5, pady=10)
        
        # Export button
        export_btn = tk.Button(
            button_frame,
            text="📊 Export Report",
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            width=15,
            command=self.export_report
        )
        export_btn.pack(side="left", padx=5, pady=10)
        
        # Admin panel button (only for admins)
        if self.auth_mgr.is_admin():
            admin_btn = tk.Button(
                button_frame,
                text="⚙️ Admin Panel",
                font=("Arial", 11, "bold"),
                bg="#9C27B0",
                fg="white",
                width=15,
                command=self.open_admin_panel
            )
            admin_btn.pack(side="left", padx=5, pady=10)
        
        # Table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        self.tree.pack(fill="both", expand=True)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Define columns
        columns = ('#', 'Client', 'Produit', 'Type de produit', 'N° de série',
                   'Garantie', 'Date produit', 'Panne', 'Réparation effectuée',
                   'PDR consommée', 'Statut', 'Centre', 'Date réception', 'Date réparation')
        
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Format columns
        for col in columns:
            self.tree.heading(col, text=col)
            if col == '#':
                self.tree.column(col, width=40, anchor='center')
            elif col in ['Client', 'N° de série']:
                self.tree.column(col, width=100)
            elif col in ['Produit', 'Type de produit', 'Panne', 'Réparation effectuée', 'PDR consommée']:
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#f0f0f0", height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            bg="#f0f0f0",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)
    
    def load_data(self):
        """Load insertion data into the table"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load insertions
        insertions = self.excel_mgr.load_insertions()
        
        for insertion in insertions:
            self.tree.insert('', 'end', values=(
                insertion.get('num', ''),
                insertion.get('client', ''),
                insertion.get('produit', ''),
                insertion.get('type_produit', ''),
                insertion.get('num_serie', ''),
                insertion.get('garantie', ''),
                insertion.get('date_produit', ''),
                insertion.get('panne', ''),
                insertion.get('reparation', ''),
                insertion.get('pdr', ''),
                insertion.get('statut', ''),
                insertion.get('centre', ''),
                insertion.get('date_reception', ''),
                insertion.get('date_reparation', '')
            ))
        
        self.status_label.config(text=f"Loaded {len(insertions)} insertions")
    
    def open_insertion_form(self):
        """Open insertion form window"""
        insertion_window = tk.Toplevel(self.root)
        InsertionWindow(insertion_window, self.excel_mgr, self.on_insertion_added)
    
    def on_insertion_added(self):
        """Callback when new insertion is added"""
        self.load_data()
        messagebox.showinfo("Success", "Insertion added successfully!")
    
    def open_admin_panel(self):
        """Open admin panel window"""
        admin_window = tk.Toplevel(self.root)
        AdminPanel(admin_window, self.excel_mgr)
    
    def export_report(self):
        """Export monthly report"""
        report_gen = ReportGenerator(self.excel_mgr)
        success, message = report_gen.generate_report()
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_mgr.logout()
            self.root.destroy()
