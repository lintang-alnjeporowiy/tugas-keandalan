import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.integrate import quad

# 1. Load data
df = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']
for col in ['n', 'b', 'h', 'a', 'Z']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Map parts to Indeks and Corrosion Rate (mm/year)
def get_corrosion_info(name):
    name_lower = name.lower()
    if 'pelat bottom' in name_lower:
        return 'PB', 0.05
    elif 'long stiff bottom' in name_lower:
        return 'SB', 0.025
    elif 'pelat deck' in name_lower:
        return 'TT', 0.05
    elif 'long stiff deck' in name_lower:
        return 'SP', 0.025
    elif 'long stiff side shell' in name_lower:
        return 'TS', 0.05
    elif 'long stiff web' in name_lower:
        return 'ST', 0.025
    elif 'long stiff cl' in name_lower:
        return 'ST', 0.025
    elif 'sekat memanjang' in name_lower:
        return 'JJ', 0.025
    elif 'pelat sisi' in name_lower:
        return 'PB', 0.05
    elif 'hopper dalam' in name_lower:
        return 'PB', 0.05
    elif 'chine luar' in name_lower:
        return 'PB', 0.05
    elif 'pembujur' in name_lower:
        return 'SB', 0.025
    else:
        if 'stiff' in name_lower or 'frame' in name_lower or 'web' in name_lower:
            return 'SB', 0.025
        else:
            return 'PB', 0.05

info = [get_corrosion_info(name) for name in df['Nama Bagian']]
df['INDEKS'] = [x[0] for x in info]
df['corrosion_rate'] = [x[1] for x in info]

# Height of ship
H_kapal = 609.6 # cm

# Yield strength data (MPa)
data_strength = np.array([
    355.504, 439.795, 472.011, 263.955, 376.981, 342.362,
    478.974, 484.172, 485.152,
    360.7, 400.4, 468.2, 426.9, 363.9, 391.1,
    462.3, 435.7, 355.7, 401.1, 472.0, 418.0
])
mu_Y = np.mean(data_strength)
std_Y = np.std(data_strength, ddof=1)

# Load data (N.m)
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
v_swbm = df_swbm['Vertical SWBM (N.m)']
max_abs_swbm = max(abs(v_swbm.min()), abs(v_swbm.max()))

df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')
wbm_vert = np.abs(df_wbm['Momen Vertikal (N.m)'])
swbm_ship = 120000 * 1000.0  # 120,000 kNm dalam N.m
vbm_total = wbm_vert + max_abs_swbm + swbm_ship

mu_L = np.mean(vbm_total)
std_L = np.std(vbm_total, ddof=1)

def calculate_modulus(t):
    corr_rate_cm = df['corrosion_rate'] / 10.0
    lebar_aktual = df['b'] - corr_rate_cm * t
    lebar_aktual = np.clip(lebar_aktual, 0, None)
    
    a_rad = np.radians(df['a'])
    A_T = df['n'] * lebar_aktual * df['h']
    S = A_T * df['Z']
    S2 = A_T * df['Z']**2
    
    Ix = (1/12) * lebar_aktual * df['h']**3 * np.cos(a_rad)**2
    Iy = (1/12) * lebar_aktual * df['h']**3 * np.sin(a_rad)**2
    I_ind = Ix + Iy
    
    Sigma1 = A_T.sum()
    Sigma2 = S.sum()
    Sigma3 = S2.sum()
    Sigma4 = I_ind.sum()
    
    Z1 = Sigma2 / Sigma1
    Z2 = H_kapal - Z1
    
    Ixx = Sigma3 + Sigma4
    I_NA = Ixx - (Z1**2) * Sigma1
    
    W_bot_m = (I_NA / Z1) / 1e6
    W_deck_m = (I_NA / Z2) / 1e6
    
    return W_bot_m, W_deck_m

ages = [0, 5, 10, 15, 20, 25, 30]
print(f"L_mean = {mu_L:.4e} N.m, L_std = {std_L:.4e} N.m")
print(f"Y_mean = {mu_Y:.4f} MPa, Y_std = {std_Y:.4f} MPa")
print("\n" + "="*80)
print(f"{'Age':<5} | {'W_bot':<10} | {'W_deck':<10} | {'FoS Bot':<10} | {'FoS Deck':<10} | {'Beta Bot':<10} | {'Beta Deck':<10}")
print("="*80)

for t in ages:
    W_bot, W_deck = calculate_modulus(t)
    
    # Bottom strength moments
    mu_S_bot = mu_Y * 1e6 * W_bot
    std_S_bot = std_Y * 1e6 * W_bot
    
    # Deck strength moments
    mu_S_deck = mu_Y * 1e6 * W_deck
    std_S_deck = std_Y * 1e6 * W_deck
    
    # FoS
    fos_bot = mu_S_bot / mu_L
    fos_deck = mu_S_deck / mu_L
    
    # Beta
    beta_bot = (mu_S_bot - mu_L) / np.sqrt(std_S_bot**2 + std_L**2)
    beta_deck = (mu_S_deck - mu_L) / np.sqrt(std_S_deck**2 + std_L**2)
    
    print(f"{t:<5} | {W_bot:<10.4f} | {W_deck:<10.4f} | {fos_bot:<10.4f} | {fos_deck:<10.4f} | {beta_bot:<10.4f} | {beta_deck:<10.4f}")
