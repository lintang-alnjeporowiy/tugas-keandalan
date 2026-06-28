import pandas as pd
import numpy as np

# Read SWBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
min_swbm_v = df_swbm['Vertical SWBM (N.m)'].min()
max_swbm_v = df_swbm['Vertical SWBM (N.m)'].max()
max_abs_swbm_v = max(abs(min_swbm_v), abs(max_swbm_v))
print(f"Max Abs SWBM V: {max_abs_swbm_v:.4f}")

# Read new Wave Bending Moment
df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')
print("Columns of new wave data:", df_wbm.columns.tolist())

vbm_total = np.abs(df_wbm['Momen Vertikal (N.m)']) + max_abs_swbm_v + 120000 * 1000.0
mu_L = np.mean(vbm_total)
std_L = np.std(vbm_total, ddof=1)
print(f"New Load Stats:")
print(f"Mean (mu_L): {mu_L:.4f} N.m")
print(f"Std Dev (sigma_L): {std_L:.4f} N.m")
