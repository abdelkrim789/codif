# Application Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAV Repair Data Management                    │
│                      Desktop Application                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   main.py        │
                    │  (Entry Point)   │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Login Screen    │
                    │  (auth.py)       │
                    └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │    Admin     │    │   Inserter   │
            │    Role      │    │     Role     │
            └──────────────┘    └──────────────┘
                    │                   │
                    │                   │
                    ▼                   ▼
            ┌──────────────────────────────────┐
            │         Dashboard                │
            │    (View All Insertions)         │
            └──────────────────────────────────┘
                    │
        ┌───────────┼───────────┬──────────────┐
        │           │           │              │
        ▼           ▼           ▼              ▼
  ┌──────────┐ ┌────────┐ ┌─────────┐  ┌────────────┐
  │   New    │ │Refresh │ │ Export  │  │   Admin    │
  │Insertion │ │  Data  │ │ Report  │  │   Panel    │
  └──────────┘ └────────┘ └─────────┘  └────────────┘
        │                       │              │
        ▼                       ▼              ▼
  ┌──────────┐           ┌──────────┐  ┌────────────┐
  │Insertion │           │ Report   │  │    CRUD    │
  │   Form   │           │Generator │  │ Operations │
  └──────────┘           └──────────┘  └────────────┘
```

## Data Flow - Cascading Dropdowns

```
User Action                    System Response
───────────                    ───────────────

1. Select Famille (FROID)  →   Filter Produits
                                ↓
2. Select Produit          →   Filter Models + Pannes
   (RÉFRIGÉRATEUR)             ↓
                                ↓
3. Select Model            →   Keep Pannes for Produit
   (GN-BCD525)                 ↓
                                ↓
4. Select Panne            →   Filter Causes
   (PAS DE FROID)              ↓
                                ↓
5. Select Cause            →   Auto-fill Solution
   (COMPRESSEUR)               ↓
                                ↓
                           Réparation effectuée:
                           "CHANGE COMPRESSEUR"
```

## Database Schema (Excel Files)

### codification_reference.xlsx

```
┌─────────────────────────────────────────────────────────┐
│ Sheet: Familles                                          │
├──────────┬──────────┐                                    │
│ ID       │ Famille  │                                    │
├──────────┼──────────┤                                    │
│ 1        │ FROID    │                                    │
└──────────┴──────────┘                                    │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Produits                                          │
├──────────┬────────────┬─────────────────────┐            │
│ ID       │ Famille_ID │ Produit             │            │
├──────────┼────────────┼─────────────────────┤            │
│ 1        │ 1          │ RÉFRIGÉRATEUR       │            │
│ 2        │ 1          │ CONGÉLATEUR         │            │
│ 3        │ 1          │ RÉFRIG. PRÉSENTOIR  │            │
│ 4        │ 1          │ FONTAINE FRAÎCHE    │            │
└──────────┴────────────┴─────────────────────┘            │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Models                                            │
├──────────┬────────────┬──────────┐                       │
│ ID       │ Produit_ID │ Model    │                       │
├──────────┼────────────┼──────────┤                       │
│ 1        │ 1          │GN-BCD525 │                       │
│ 2        │ 1          │GN-BCD435 │                       │
│ ...      │ ...        │ ...      │                       │
└──────────┴────────────┴──────────┘                       │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Pannes                                            │
├──────────┬──────────┬────────────┬──────────────┐        │
│ ID       │ Code     │ Produit_ID │ Panne        │        │
├──────────┼──────────┼────────────┼──────────────┤        │
│ 1        │ REF-001  │ 1          │PAS DE FROID  │        │
│ 2        │ REF-009  │ 1          │BRUIT         │        │
│ 3        │ REF-011  │ 1          │GIVRE         │        │
└──────────┴──────────┴────────────┴──────────────┘        │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Causes                                            │
├──────────┬──────────────┬──────────┬──────────────┐      │
│ ID       │ Code         │ Panne_ID │ Cause        │      │
├──────────┼──────────────┼──────────┼──────────────┤      │
│ 1        │ REF-001-C01  │ 1        │COMPRESSEUR   │      │
│ 2        │ REF-001-C02  │ 1        │RELAIS+CLIXON │      │
└──────────┴──────────────┴──────────┴──────────────┘      │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Solutions                                         │
├──────────┬──────────────┬──────────┬───────────────────┐ │
│ ID       │ Code         │ Cause_ID │ Solution          │ │
├──────────┼──────────────┼──────────┼───────────────────┤ │
│ 1        │ REF-001-S01  │ 1        │CHANGE COMPRESSEUR │ │
│ 2        │ REF-001-S02  │ 2        │CHANGE RELAIS+...  │ │
└──────────┴──────────────┴──────────┴───────────────────┘ │
                                                            │
┌─────────────────────────────────────────────────────────┤
│ Sheet: Users                                             │
├──────────┬──────────┬──────────┬──────┐                 │
│ ID       │ Username │ Password │ Role │                 │
├──────────┼──────────┼──────────┼──────┤                 │
│ 1        │ admin    │ admin123 │admin │                 │
└──────────┴──────────┴──────────┴──────┘                 │
└─────────────────────────────────────────────────────────┘
```

### rapport_insertions.xlsx

```
┌────────────────────────────────────────────────────────────────┐
│ Direction SAV Géant Froid                                       │
│ Centre SAV [Centre Name]                                        │
│ Rapport Mois [Month Year]                                       │
├──┬────────┬─────────┬──────────┬────────┬─────────┬───────────┤
│#│Client  │Produit  │Type de   │N° de   │Garantie │Date       │
│ │        │         │produit   │série   │         │produit    │
├──┼────────┼─────────┼──────────┼────────┼─────────┼───────────┤
│1│Ahmed   │RÉFRIGÉ- │GN-BCD525 │SN12345 │Garantie │2024-01-15 │
│ │        │RATEUR   │          │        │         │           │
├──┴────────┴─────────┴──────────┴────────┴─────────┴───────────┤
│  Panne │Réparation │PDR      │Statut │Centre │Date    │Date   │
│        │effectuée  │consommée│       │       │récep.  │répar. │
├────────┼───────────┼─────────┼───────┼───────┼────────┼───────┤
│PAS DE  │CHANGE     │PDR-123  │Réparé │Centre │2024-02-│2024-  │
│FROID   │COMPRESSEUR│         │       │Princi.│01      │02-05  │
└────────┴───────────┴─────────┴───────┴───────┴────────┴───────┘
```

## Component Relationships

```
┌──────────────────────────────────────────────────────┐
│                    GUI Layer                          │
│  ┌────────────┐  ┌───────────┐  ┌──────────────┐    │
│  │ login.py   │  │dashboard  │  │ insertion.py │    │
│  └────────────┘  │   .py     │  └──────────────┘    │
│  ┌────────────┐  └───────────┘  ┌──────────────┐    │
│  │admin_panel │                  │  report.py   │    │
│  │   .py      │                  └──────────────┘    │
│  └────────────┘                                      │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│                 Business Logic                        │
│  ┌────────────────────────────────────────────────┐  │
│  │  auth.py - User authentication & authorization │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│                   Data Layer                          │
│  ┌────────────────────────────────────────────────┐  │
│  │  excel_manager.py - Excel CRUD operations      │  │
│  │   - load_reference_data()                      │  │
│  │   - save_reference_data()                      │  │
│  │   - load_insertions()                          │  │
│  │   - add_insertion()                            │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│                Storage Layer (Excel)                  │
│  ┌──────────────────────┐  ┌────────────────────┐   │
│  │codification_reference│  │rapport_insertions  │   │
│  │       .xlsx          │  │      .xlsx         │   │
│  └──────────────────────┘  └────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## User Journey

### Inserter Workflow

```
1. Login with credentials
   ↓
2. See dashboard with existing repairs
   ↓
3. Click "New Insertion"
   ↓
4. Fill cascading form:
   - Select Famille → Produit → Model
   - Select Panne → Cause
   - Solution auto-fills
   - Fill remaining fields
   ↓
5. Save insertion
   ↓
6. Data appears in dashboard
   ↓
7. Logout
```

### Admin Workflow

```
1. Login as admin
   ↓
2. Access Admin Panel
   ↓
3. Manage reference data:
   - Add new product families
   - Add models
   - Add fault codes
   - Create user accounts
   ↓
4. Save changes
   ↓
5. Changes reflect in insertion form dropdowns
   ↓
6. Export monthly reports
```

## Security Model

```
┌────────────────────────────────────────┐
│          User Roles                    │
├────────────────────────────────────────┤
│                                        │
│  Admin:                                │
│   ✓ View all data                     │
│   ✓ Insert repairs                    │
│   ✓ CRUD reference data               │
│   ✓ Manage users                      │
│   ✓ Export reports                    │
│                                        │
│  Inserter:                             │
│   ✓ View all data                     │
│   ✓ Insert repairs                    │
│   ✗ CRUD reference data               │
│   ✗ Manage users                      │
│   ✓ Export reports                    │
│                                        │
└────────────────────────────────────────┘
```
