# Ship Structural Reliability Analysis - Progress Summary (Updated)

This folder contains the complete state and all artifacts for the Ship Structural Reliability Analysis project over a 30-year lifecycle under 24 load variations.

## 📅 Project State
- **Status**: **Fully Completed** and verified.
- **Main Output**: [/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/main.ipynb](file:///mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/main.ipynb) - Contains load analysis (6 wave cases), strength calculations with bi-directional corrosion (cor-rate.csv), governing modulus selection, ultimate strength reliability (412.14 MPa), yield strength reliability (250 MPa), and scantlings dimension CSV export.
- **CSV Data Output**: [/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantling_corroded.csv](file:///mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantling_corroded.csv) - Contains all member scantlings with b and h values at ages 0, 10, 20, and 30 years.

---

## 📂 Progress Artifacts Directory Structure
```
progress/
├── implementation_plan.md    # The updated and approved plan
├── task.md                   # Checklist of steps executed
├── walkthrough.md            # Final summary of calculations and findings
├── summary.md                # This file (master context guide)
└── scratch/                  # Executable helper & verification scripts
    ├── generate_notebook.py  # Python script that generates main.ipynb cell by cell
    ├── patch_to_24_cases.py  # Script used to modify generate_notebook.py
    ├── clean_markdown_cells.py # Script used to clean notebook validation keys
    ├── read_notebook_outputs.py # Script used to print cell execution results
    └── verify_calculations_new.py # Script used to verify mathematical values
```

---

## 🚀 Key Calculations & Formulas Used

### 1. Load Combination (Updated for 6 Wave Configurations)
To calculate the total vertical bending moment ($VBM_{\text{total}}$), we combine three components: the wave bending moment (WBM), the static maximum SWBM from `SWBM.csv`, and the ship's own constant SWBM (defined as a variable `swbm_ship = 1.2e8` N.m):
- **Absolute Max Static SWBM**: Found to be $1.5464 \times 10^8$ N.m ($154,641.12$ kNm).
- **Ship SWBM Constant (Variable)**: $1.2000 \times 10^8$ N.m ($120,000.00$ kNm).
- **Formula for Head Wave ($D = 180^\circ$)**: $VBM_{\text{total}} = |WBM_{\text{dynamic, vertical}}| + |SWBM_{\text{static\_max, vertical}}| + swbm\_ship$.
- **Formula for Beam Wave ($D = 90^\circ$)**: $VBM_{\text{total}} = |WBM_{\text{dynamic, horizontal}}| + |SWBM_{\text{static\_max, vertical}}| + swbm\_ship$.

### 2. Corrosion Rate Mapping & Bi-directional Corrosion
Laju korosi memengaruhi lebar ($b$) dan tinggi ($h$) dari elemen scantling sekaligus:
$$b_{\text{aktual}} = \max(b - \text{corrosion\_rate\_cm} \times t, 0)$$
$$h_{\text{aktual}} = \max(h - \text{corrosion\_rate\_cm} \times t, 0)$$

### 3. Neutral Axis (NA) and Governing Modulus
At each age $T \in [0, 10, 20, 30]$ years:
- Recompute area, neutral axis ($Z_1, Z_2$), moment of inertia ($I_{\text{NA}}$), and section moduli ($W_{\text{bot}}, W_{\text{deck}}$).
- **Governing Modulus ($W_{\text{pantau}}$)**:
   $$W_{\text{pantau}} = \min(W_{\text{bot}}, W_{\text{deck}})$$

### 4. Reliability in MPa Units (Ultimate Strength = 412.14 MPa)
- **Load Stress**:
  $$\mu_{\sigma_L} = \frac{\mu_L}{W_{\text{pantau}}} \times 10^{-6} \text{ MPa}$$
  $$\sigma_{\sigma_L} = \frac{\sigma_L}{W_{\text{pantau}}} \times 10^{-6} \text{ MPa}$$
- **Strength Stress (A36 Steel)**:
  - Mean ($\mu_Y$) = $412.1384$ MPa
  - Std Dev ($\sigma_Y$) = $58.9565$ MPa
- **Safety Factor (FoS)**:
  $$FoS = \frac{\mu_Y}{\mu_{\sigma_L}}$$
- **Safety Index ($\beta$)**:
  $$\beta = \frac{\mu_Y - \mu_{\sigma_L}}{\sqrt{\sigma_Y^2 + \sigma_{\sigma_L}^2}}$$

### 5. Reliability in MPa Units (Yield Strength = 250 MPa)
- **Coefficient of Variation (CoV)**: Derived from ultimate strength data:
  $$\text{CoV} = \frac{58.9565}{412.1384} \approx 0.143050$$
- **Yield Strength Distribution**:
  - Mean ($\mu_{Y\_yield}$) = $250.0$ MPa
  - Std Dev ($\sigma_{Y\_yield}$) = $250.0 \times \text{CoV} \approx 35.7625$ MPa

---

## 🛠️ Verification
All steps have been successfully verified. To run the notebook and check for issues:
1. Run `python3 progress/scratch/generate_notebook.py` to compile `main.ipynb`.
2. Run `jupyter nbconvert --to notebook --execute --inplace main.ipynb` to run all cells.
