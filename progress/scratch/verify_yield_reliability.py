import pandas as pd
import numpy as np
import scipy.integrate as integrate
from scipy.stats import norm

# Load SWBM and WBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
min_swbm_v = df_swbm['Vertical SWBM (N.m)'].min()
max_swbm_v = df_swbm['Vertical SWBM (N.m)'].max()
max_abs_swbm_v = max(abs(min_swbm_v), abs(max_swbm_v))

df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')
swbm_ship = 120000 * 1000.0  # 120,000 kNm dalam N.m
vbm_total = np.abs(df_wbm['Momen Vertikal (N.m)']) + max_abs_swbm_v + swbm_ship

mu_L = np.mean(vbm_total)
sigma_L = np.std(vbm_total, ddof=1)

# Scantlings
df_scant = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df_scant.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']
df_cor = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/cor-rate.csv')

def map_element(name):
    name_lower = name.lower()
    if 'pelat bottom' in name_lower or 'chine luar' in name_lower:
        return 'OPB'
    elif 'long stiff bottom' in name_lower or 'pembujur' in name_lower:
        if 'web' in name_lower:
            return 'SBW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SBF'
        else:
            return 'SBW'
    elif 'hopper dalam' in name_lower or 'inner bottom' in name_lower:
        return 'IPB'
    elif 'pelat deck' in name_lower:
        return 'DP'
    elif 'long stiff deck' in name_lower:
        if 'web' in name_lower:
            return 'DPW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'DPF'
        else:
            return 'DPW'
    elif 'sekat memanjang' in name_lower or 'sekat' in name_lower:
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'SLW'
    elif 'pelat sisi' in name_lower:
        return 'OPB'
    elif 'long stiff side shell' in name_lower or 'long stiff web' in name_lower or 'long stiff cl' in name_lower:
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'SLW'
    else:
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'OPB'

df_scant['mapped_index'] = df_scant['Nama Bagian'].apply(map_element)
df_scant = df_scant.merge(df_cor, left_on='mapped_index', right_on='index', how='left')

H_kapal = 609.6

def calculate_modulus_at_age(t):
    corr_rate_cm = df_scant['μ (a) [mm/years]'] / 10.0
    b_aktual = np.clip(df_scant['b'] - corr_rate_cm * t, 0, None)
    h_aktual = np.clip(df_scant['h'] - corr_rate_cm * t, 0, None)
    a_rad = np.radians(df_scant['a'])
    
    A_T = df_scant['n'] * b_aktual * h_aktual
    S = A_T * df_scant['Z']
    S2 = A_T * df_scant['Z']**2
    Ix = (1/12) * b_aktual * h_aktual**3 * np.cos(a_rad)**2
    Iy = (1/12) * b_aktual * h_aktual**3 * np.sin(a_rad)**2
    I_ind = Ix + Iy
    
    Sigma1 = A_T.sum()
    Sigma2 = S.sum()
    Sigma3 = S2.sum()
    Sigma4 = I_ind.sum()
    
    Z1 = Sigma2 / Sigma1
    Z2 = H_kapal - Z1
    Ixx = Sigma3 + Sigma4
    I_NA = Ixx - (Z1**2) * Sigma1
    
    return I_NA / Z1 / 1e6, I_NA / Z2 / 1e6

ages = [0, 10, 20, 30]
W_pantau_vals = []
for t in ages:
    wb, wd = calculate_modulus_at_age(t)
    W_pantau_vals.append(min(wb, wd))

# Yield strength analysis
data_strength = np.array([
    355.504, 439.795, 472.011, 263.955, 376.981, 342.362,
    478.974, 484.172, 485.152,
    360.7, 400.4, 468.2, 426.9, 363.9, 391.1,
    462.3, 435.7, 355.7, 401.1, 472.0, 418.0
])
mu_Y_ult = np.mean(data_strength)
sigma_Y_ult = np.std(data_strength, ddof=1)
cov_Y = sigma_Y_ult / mu_Y_ult

# New Yield Strength stats
mu_Y_new = 250.0
sigma_Y_new = mu_Y_new * cov_Y

print(f"CoV of Ultimate Strength: {cov_Y:.6f}")
print(f"New Yield Strength Mean: {mu_Y_new:.2f} MPa")
print(f"New Yield Strength Std Dev: {sigma_Y_new:.6f} MPa")

results = []
for t, W_pantau in zip(ages, W_pantau_vals):
    mu_sigma_L = (mu_L / W_pantau) * 1e-6
    sigma_sigma_L = (sigma_L / W_pantau) * 1e-6
    
    FoS = mu_Y_new / mu_sigma_L
    beta = (mu_Y_new - mu_sigma_L) / np.sqrt(sigma_Y_new**2 + sigma_sigma_L**2)
    Pf = norm.cdf(-beta)
    
    results.append({
        'Age': t,
        'W_pantau': W_pantau,
        'mu_sigma_L': mu_sigma_L,
        'sigma_sigma_L': sigma_sigma_L,
        'FoS': FoS,
        'Beta': beta,
        'Pf': Pf
    })

df_res = pd.DataFrame(results)
print("\n--- New Reliability Analysis (Yield Strength = 250 MPa) ---")
print(df_res.to_string(index=False))
