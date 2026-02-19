"""Admin panel for CRUD operations"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class AdminPanel:
    """Admin panel for managing reference data"""
    
    def __init__(self, root, excel_mgr):
        self.root = root
        self.excel_mgr = excel_mgr
        
        self.root.title("Admin Panel")
        self.root.geometry("900x600")
        
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
        self.create_users_tab(notebook)
        
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
    
    def create_familles_tab(self, notebook):
        """Create familles management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Familles")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_famille())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.familles_tree, 'familles'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.familles_tree = ttk.Treeview(frame, columns=('ID', 'Famille'), show='headings')
        self.familles_tree.heading('ID', text='ID')
        self.familles_tree.heading('Famille', text='Famille')
        self.familles_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for f in self.ref_data.get('familles', []):
            self.familles_tree.insert('', 'end', values=(f['id'], f['famille']))
    
    def create_produits_tab(self, notebook):
        """Create produits management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Produits")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_produit())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.produits_tree, 'produits'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.produits_tree = ttk.Treeview(frame, columns=('ID', 'Famille ID', 'Produit'), show='headings')
        self.produits_tree.heading('ID', text='ID')
        self.produits_tree.heading('Famille ID', text='Famille ID')
        self.produits_tree.heading('Produit', text='Produit')
        self.produits_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for p in self.ref_data.get('produits', []):
            self.produits_tree.insert('', 'end', values=(p['id'], p['famille_id'], p['produit']))
    
    def create_models_tab(self, notebook):
        """Create models management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Models")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_model())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.models_tree, 'models'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.models_tree = ttk.Treeview(frame, columns=('ID', 'Produit ID', 'Model'), show='headings')
        self.models_tree.heading('ID', text='ID')
        self.models_tree.heading('Produit ID', text='Produit ID')
        self.models_tree.heading('Model', text='Model')
        self.models_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for m in self.ref_data.get('models', []):
            self.models_tree.insert('', 'end', values=(m['id'], m['produit_id'], m['model']))
    
    def create_pannes_tab(self, notebook):
        """Create pannes management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Pannes")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_panne())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.pannes_tree, 'pannes'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.pannes_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Produit ID', 'Panne'), show='headings')
        self.pannes_tree.heading('ID', text='ID')
        self.pannes_tree.heading('Code', text='Code')
        self.pannes_tree.heading('Produit ID', text='Produit ID')
        self.pannes_tree.heading('Panne', text='Panne')
        self.pannes_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for p in self.ref_data.get('pannes', []):
            self.pannes_tree.insert('', 'end', values=(p['id'], p['code'], p['produit_id'], p['panne']))
    
    def create_causes_tab(self, notebook):
        """Create causes management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Causes")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_cause())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.causes_tree, 'causes'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.causes_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Panne ID', 'Cause'), show='headings')
        self.causes_tree.heading('ID', text='ID')
        self.causes_tree.heading('Code', text='Code')
        self.causes_tree.heading('Panne ID', text='Panne ID')
        self.causes_tree.heading('Cause', text='Cause')
        self.causes_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for c in self.ref_data.get('causes', []):
            self.causes_tree.insert('', 'end', values=(c['id'], c['code'], c['panne_id'], c['cause']))
    
    def create_solutions_tab(self, notebook):
        """Create solutions management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Solutions")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_solution())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.solutions_tree, 'solutions'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.solutions_tree = ttk.Treeview(frame, columns=('ID', 'Code', 'Cause ID', 'Solution'), show='headings')
        self.solutions_tree.heading('ID', text='ID')
        self.solutions_tree.heading('Code', text='Code')
        self.solutions_tree.heading('Cause ID', text='Cause ID')
        self.solutions_tree.heading('Solution', text='Solution')
        self.solutions_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for s in self.ref_data.get('solutions', []):
            self.solutions_tree.insert('', 'end', values=(s['id'], s['code'], s['cause_id'], s['solution']))
    
    def create_centres_tab(self, notebook):
        """Create centres management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Centres")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add", command=lambda: self.add_centre())
        add_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.centres_tree, 'centres'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.centres_tree = ttk.Treeview(frame, columns=('ID', 'Centre'), show='headings')
        self.centres_tree.heading('ID', text='ID')
        self.centres_tree.heading('Centre', text='Centre')
        self.centres_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for c in self.ref_data.get('centres', []):
            self.centres_tree.insert('', 'end', values=(c['id'], c['centre']))
    
    def create_users_tab(self, notebook):
        """Create users management tab"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="Users")
        
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        add_btn = tk.Button(toolbar, text="Add User", command=lambda: self.add_user())
        add_btn.pack(side="left", padx=2)
        
        reset_btn = tk.Button(toolbar, text="Reset Password", command=lambda: self.reset_password())
        reset_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(toolbar, text="Delete", command=lambda: self.delete_selected(self.users_tree, 'users'))
        delete_btn.pack(side="left", padx=2)
        
        # Tree
        self.users_tree = ttk.Treeview(frame, columns=('ID', 'Username', 'Role'), show='headings')
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Username', text='Username')
        self.users_tree.heading('Role', text='Role')
        self.users_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load data
        for u in self.ref_data.get('users', []):
            self.users_tree.insert('', 'end', values=(u['id'], u['username'], u['role']))
    
    def add_famille(self):
        """Add new famille"""
        name = simpledialog.askstring("Add Famille", "Enter famille name:")
        if name:
            new_id = max([f['id'] for f in self.ref_data['familles']], default=0) + 1
            new_famille = {'id': new_id, 'famille': name}
            self.ref_data['familles'].append(new_famille)
            self.familles_tree.insert('', 'end', values=(new_id, name))
    
    def add_produit(self):
        """Add new produit"""
        famille_id = simpledialog.askinteger("Add Produit", "Enter Famille ID:")
        if famille_id:
            name = simpledialog.askstring("Add Produit", "Enter produit name:")
            if name:
                new_id = max([p['id'] for p in self.ref_data['produits']], default=0) + 1
                new_produit = {'id': new_id, 'famille_id': famille_id, 'produit': name}
                self.ref_data['produits'].append(new_produit)
                self.produits_tree.insert('', 'end', values=(new_id, famille_id, name))
    
    def add_model(self):
        """Add new model"""
        produit_id = simpledialog.askinteger("Add Model", "Enter Produit ID:")
        if produit_id:
            name = simpledialog.askstring("Add Model", "Enter model name:")
            if name:
                new_id = max([m['id'] for m in self.ref_data['models']], default=0) + 1
                new_model = {'id': new_id, 'produit_id': produit_id, 'model': name}
                self.ref_data['models'].append(new_model)
                self.models_tree.insert('', 'end', values=(new_id, produit_id, name))
    
    def add_panne(self):
        """Add new panne"""
        produit_id = simpledialog.askinteger("Add Panne", "Enter Produit ID:")
        if produit_id:
            code = simpledialog.askstring("Add Panne", "Enter panne code:")
            if code:
                name = simpledialog.askstring("Add Panne", "Enter panne name:")
                if name:
                    new_id = max([p['id'] for p in self.ref_data['pannes']], default=0) + 1
                    new_panne = {'id': new_id, 'code': code, 'produit_id': produit_id, 'panne': name}
                    self.ref_data['pannes'].append(new_panne)
                    self.pannes_tree.insert('', 'end', values=(new_id, code, produit_id, name))
    
    def add_cause(self):
        """Add new cause"""
        panne_id = simpledialog.askinteger("Add Cause", "Enter Panne ID:")
        if panne_id:
            code = simpledialog.askstring("Add Cause", "Enter cause code:")
            if code:
                name = simpledialog.askstring("Add Cause", "Enter cause name:")
                if name:
                    new_id = max([c['id'] for c in self.ref_data['causes']], default=0) + 1
                    new_cause = {'id': new_id, 'code': code, 'panne_id': panne_id, 'cause': name}
                    self.ref_data['causes'].append(new_cause)
                    self.causes_tree.insert('', 'end', values=(new_id, code, panne_id, name))
    
    def add_solution(self):
        """Add new solution"""
        cause_id = simpledialog.askinteger("Add Solution", "Enter Cause ID:")
        if cause_id:
            code = simpledialog.askstring("Add Solution", "Enter solution code:")
            if code:
                name = simpledialog.askstring("Add Solution", "Enter solution name:")
                if name:
                    new_id = max([s['id'] for s in self.ref_data['solutions']], default=0) + 1
                    new_solution = {'id': new_id, 'code': code, 'cause_id': cause_id, 'solution': name}
                    self.ref_data['solutions'].append(new_solution)
                    self.solutions_tree.insert('', 'end', values=(new_id, code, cause_id, name))
    
    def add_centre(self):
        """Add new centre"""
        name = simpledialog.askstring("Add Centre", "Enter centre name:")
        if name:
            new_id = max([c['id'] for c in self.ref_data['centres']], default=0) + 1
            new_centre = {'id': new_id, 'centre': name}
            self.ref_data['centres'].append(new_centre)
            self.centres_tree.insert('', 'end', values=(new_id, name))
    
    def add_user(self):
        """Add new user"""
        username = simpledialog.askstring("Add User", "Enter username:")
        if username:
            password = simpledialog.askstring("Add User", "Enter password:")
            if password:
                role = simpledialog.askstring("Add User", "Enter role (admin/inserter):")
                if role in ['admin', 'inserter']:
                    new_id = max([u['id'] for u in self.ref_data['users']], default=0) + 1
                    new_user = {'id': new_id, 'username': username, 'password': password, 'role': role}
                    self.ref_data['users'].append(new_user)
                    self.users_tree.insert('', 'end', values=(new_id, username, role))
    
    def reset_password(self):
        """Reset user password"""
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
        """Delete selected item"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item = tree.item(selection[0])
            item_id = item['values'][0]
            
            # Remove from data
            self.ref_data[data_key] = [x for x in self.ref_data[data_key] if x['id'] != item_id]
            
            # Remove from tree
            tree.delete(selection[0])
    
    def save_changes(self):
        """Save all changes to Excel"""
        try:
            self.excel_mgr.save_reference_data(self.ref_data)
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
