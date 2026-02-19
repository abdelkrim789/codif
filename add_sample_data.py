#!/usr/bin/env python3
"""Add sample insertion data for testing"""
import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.excel_manager import ExcelManager

def add_sample_data():
    """Add sample repair insertions"""
    excel_mgr = ExcelManager()
    
    # Load reference data
    ref_data = excel_mgr.load_reference_data()
    
    # Sample clients
    clients = [
        "Mohamed Alami",
        "Fatima Zahra",
        "Ahmed Benali",
        "Sara El Amrani",
        "Omar Chakir"
    ]
    
    # Sample serial numbers
    def generate_serial():
        return f"SN{random.randint(10000, 99999)}"
    
    # Garantie options
    garanties = ["Garantie", "Hors Garantie", "Fiche de garantie"]
    
    # Statuts
    statuts = ["Réparé", "En cours", "Non réparé", "Pièce non disponible", "Changé"]
    
    # Get a random model and its related data
    models = ref_data['models']
    
    print("Adding sample insertions...")
    
    for i in range(10):
        # Random model
        model = random.choice(models)
        produit = next(p for p in ref_data['produits'] if p['id'] == model['produit_id'])
        
        # Get pannes for this produit
        pannes = [p for p in ref_data['pannes'] if p['produit_id'] == produit['id']]
        if not pannes:
            continue
        
        panne = random.choice(pannes)
        
        # Get causes for this panne
        causes = [c for c in ref_data['causes'] if c['panne_id'] == panne['id']]
        if not causes:
            continue
        
        cause = random.choice(causes)
        
        # Get solution for this cause
        solutions = [s for s in ref_data['solutions'] if s['cause_id'] == cause['id']]
        solution_text = solutions[0]['solution'] if solutions else "N/A"
        
        # Random dates
        date_reception = datetime.now() - timedelta(days=random.randint(1, 30))
        date_reparation = date_reception + timedelta(days=random.randint(1, 7))
        date_produit = date_reception - timedelta(days=random.randint(30, 365))
        
        insertion_data = {
            'client': random.choice(clients),
            'produit': produit['produit'],
            'type_produit': model['model'],
            'num_serie': generate_serial(),
            'garantie': random.choice(garanties),
            'date_produit': date_produit.strftime("%Y-%m-%d"),
            'panne': panne['panne'],
            'reparation': solution_text,
            'pdr': 'PDR-' + str(random.randint(100, 999)),
            'statut': random.choice(statuts),
            'centre': 'Centre Principal',
            'date_reception': date_reception.strftime("%Y-%m-%d"),
            'date_reparation': date_reparation.strftime("%Y-%m-%d")
        }
        
        excel_mgr.add_insertion(insertion_data)
        print(f"  Added insertion {i+1}: {insertion_data['client']} - {insertion_data['produit']} - {insertion_data['panne']}")
    
    print(f"\n✅ Successfully added 10 sample insertions!")
    print("You can view them in the dashboard.")

if __name__ == '__main__':
    add_sample_data()
