import pandas as pd
import numpy as np

# Load scantling data
df = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']

# Ensure numeric columns
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
        # Fallback based on name keywords
        if 'stiff' in name_lower or 'frame' in name_lower or 'web' in name_lower:
            return 'SB', 0.025
        else:
            return 'PB', 0.05

info = [get_corrosion_info(name) for name in df['Nama Bagian']]
df['INDEKS'] = [x[0] for x in info]
df['corrosion_rate'] = [x[1] for x in info]

# Height of ship
H_kapal = 609.6 # cm

def calculate_modulus(t):
    # Corrosion rate in cm/year: corrosion_rate / 10
    # lebar_aktual = b - (corrosion_rate_cm * t)
    corr_rate_cm = df['corrosion_rate'] / 10.0
    lebar_aktual = df['b'] - corr_rate_cm * t
    
    # Clip lebar_aktual to not be negative
    lebar_aktual = np.clip(lebar_aktual, 0, None)
    
    # Calculate properties
    a_rad = np.radians(df['a'])
    
    A_T = df['n'] * lebar_aktual * df['h']
    S = A_T * df['Z']
    S2 = A_T * df['Z']**2
    
    # Ix & Iy (note: individual moment of inertia uses b, which is lebar_aktual now.
    # Wait! In section_modulus.ipynb: Ix = (1/12) * b * h^3 * cos^2(a). Does it include n?
    # In section_modulus.ipynb, the formula in markdown is: Ix = (1/12) * b * h^3 * cos^2(a),
    # but let's check cell 4 of section_modulus.ipynb code:
    # df['Ix (cm⁴)'] = (1/12) * df['b'] * df['h']**3 * np.cos(a_rad)**2
    # So it doesn't multiply by n. Let's make sure we use the same formula.
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
    
    W_bot_cm = I_NA / Z1
    W_deck_cm = I_NA / Z2
    
    W_bot_m = W_bot_cm / 1e6
    W_deck_m = W_deck_cm / 1e6
    
    return W_bot_m, W_deck_m, Z1, Z2, I_NA

print("T=0 calculation:")
W_bot_0, W_deck_0, Z1_0, Z2_0, I_NA_0 = calculate_modulus(0)
print(f"W_bot (m3): {W_bot_0:.6f}")
print(f"W_deck (m3): {W_deck_0:.6f}")
print(f"Z1: {Z1_0:.4f}, Z2: {Z2_0:.4f}, I_NA: {I_NA_0:.4f}")
