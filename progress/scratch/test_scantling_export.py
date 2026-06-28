import pandas as pd
import numpy as np

# Read scantling and corrosion rate
df_scant = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df_scant.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']
df_cor = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/cor-rate.csv')

# Pemetaan
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

# Generate columns b and h for ages 0, 10, 20, 30
corr_rate_cm = df_scant['μ (a) [mm/years]'] / 10.0

for t in [0, 10, 20, 30]:
    df_scant[f'b_t{t}'] = np.clip(df_scant['b'] - corr_rate_cm * t, 0, None)
    df_scant[f'h_t{t}'] = np.clip(df_scant['h'] - corr_rate_cm * t, 0, None)

# Show the table columns
print("Export columns:", df_scant.columns.tolist())
# Export to CSV
df_scant.to_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantling_corroded.csv', sep=';', index=False)
print("Exported to scantling_corroded.csv successfully!")
