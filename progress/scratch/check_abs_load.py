import pandas as pd
import numpy as np

# Read SWBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
min_swbm_v = df_swbm['Vertical SWBM (N.m)'].min()
max_swbm_v = df_swbm['Vertical SWBM (N.m)'].max()
max_abs_swbm_v = max(abs(min_swbm_v), abs(max_swbm_v))

# Read wave-102
df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')

# Old way
vbm_total_old = df_wbm['Momen Vertikal (N.m)'] + max_abs_swbm_v
mu_old = np.mean(vbm_total_old)
std_old = np.std(vbm_total_old, ddof=1)

# New way: take absolute value of wave bending moment first
abs_wbm_v = np.abs(df_wbm['Momen Vertikal (N.m)'])
vbm_total_new = abs_wbm_v + max_abs_swbm_v
mu_new = np.mean(vbm_total_new)
std_new = np.std(vbm_total_new, ddof=1)

print(f"Old Way Load Stats:")
print(f"Mean: {mu_old:.4e} N.m")
print(f"Std Dev: {std_old:.4e} N.m")
print(f"\nNew Way (with absolute wave moment) Load Stats:")
print(f"Mean: {mu_new:.4e} N.m")
print(f"Std Dev: {std_new:.4e} N.m")
