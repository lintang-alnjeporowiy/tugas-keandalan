import pandas as pd
import numpy as np
import scipy.integrate as integrate
from scipy.stats import norm

print("--- Step 1: Load Analysis ---")
# Read SWBM and WBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
min_swbm_v = df_swbm['Vertical SWBM (N.m)'].min()
max_swbm_v = df_swbm['Vertical SWBM (N.m)'].max()
max_abs_swbm_v = max(abs(min_swbm_v), abs(max_swbm_v))

df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')
swbm_ship = 120000 * 1000.0  # 120,000 kNm dalam N.m
vbm_total = np.abs(df_wbm['Momen Vertikal (N.m)']) + max_abs_swbm_v + swbm_ship

mu_L = np.mean(vbm_total)
sigma_L = np.std(vbm_total, ddof=1)
print(f"Max Abs SWBM V: {max_abs_swbm_v:.4f} N.m")
print(f"Total Load - Mean: {mu_L:.4f} N.m, Std Dev: {sigma_L:.4f} N.m")

print("\n--- Step 2: Strength Analysis ---")
# Read scantling and corrosion rate
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

# Check mapping completeness
if df_scant['μ (a) [mm/years]'].isna().any():
    print("Warning: some elements were not mapped correctly!")
else:
    print("All elements mapped to corrosion rates successfully!")

H_kapal = 609.6 # cm

# Yield strength stats (A36) in MPa
mu_Y = 412.1384
sigma_Y = 58.9565

ages = [0, 10, 20, 30]
results = []

for t in ages:
    # Corrosion rate in cm/year (cor_rate_mm / 10)
    corr_rate_cm = df_scant['μ (a) [mm/years]'] / 10.0
    
    # Bi-directional corrosion: b and h are corroded
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
    
    W_bot_cm = I_NA / Z1
    W_deck_cm = I_NA / Z2
    
    W_bot_m = W_bot_cm / 1e6
    W_deck_m = W_deck_cm / 1e6
    
    # Governing section modulus
    W_pantau = min(W_bot_m, W_deck_m)
    
    # Stress calculation in MPa
    # σ = M / W * 10^-6
    mu_sigma_L = (mu_L / W_pantau) * 1e-6
    sigma_sigma_L = (sigma_L / W_pantau) * 1e-6
    
    # Safety Factor (FoS)
    FoS = mu_Y / mu_sigma_L
    
    # Safety Index (Beta)
    beta = (mu_Y - mu_sigma_L) / np.sqrt(sigma_Y**2 + sigma_sigma_L**2)
    
    # Failure Probability (Pf) - Analytical
    Pf_analytical = norm.cdf(-beta)
    
    # Failure Probability (Pf) - Numerical Convolution
    def integrand(x):
        # norm.pdf(x, mu_sigma_L, sigma_sigma_L) * norm.cdf(x, mu_Y, sigma_Y)
        # Wait, Pf = P(S < L) = \int f_L(x) * F_S(x) dx
        return norm.pdf(x, mu_sigma_L, sigma_sigma_L) * norm.cdf(x, mu_Y, sigma_Y)
    
    # Integrate over a reasonable range, e.g. [mu_sigma_L - 8*sigma_sigma_L, mu_sigma_L + 8*sigma_sigma_L]
    limit_low = mu_sigma_L - 8 * sigma_sigma_L
    limit_high = mu_sigma_L + 8 * sigma_sigma_L
    Pf_numerical, _ = integrate.quad(integrand, limit_low, limit_high)
    
    results.append({
        'Age': t,
        'W_bot': W_bot_m,
        'W_deck': W_deck_m,
        'W_pantau': W_pantau,
        'mu_sigma_L': mu_sigma_L,
        'sigma_sigma_L': sigma_sigma_L,
        'FoS': FoS,
        'Beta': beta,
        'Pf_analytical': Pf_analytical,
        'Pf_numerical': Pf_numerical
    })

df_res = pd.DataFrame(results)
print("\n--- Summary of Results ---")
print(df_res.to_string(index=False))
