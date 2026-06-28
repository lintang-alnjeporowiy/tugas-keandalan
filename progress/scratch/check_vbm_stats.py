import pandas as pd
import numpy as np

# Load SWBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
v_swbm = df_swbm['Vertical SWBM (N.m)']
min_v = v_swbm.min()
max_v = v_swbm.max()
max_abs = max(abs(min_v), abs(max_v))

# Load WBM
df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/wave-102.csv', sep=';')
wbm_vert = np.abs(df_wbm['Momen Vertikal (N.m)'])

# Still Water Bending Moment Kapal (konstanta)
swbm_ship = 120000 * 1000.0  # 120,000 kNm dalam N.m

# Total vertical bending moment
vbm_total = wbm_vert + max_abs + swbm_ship

mu_L = np.mean(vbm_total)
std_L = np.std(vbm_total, ddof=1)

print(f"Mean Total VBM (mu_L): {mu_L:.6e} N.m")
print(f"Std Dev Total VBM (std_L): {std_L:.6e} N.m")
