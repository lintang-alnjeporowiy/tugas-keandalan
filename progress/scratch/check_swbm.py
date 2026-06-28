import pandas as pd

df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
v_swbm = df_swbm['Vertical SWBM (N.m)']
min_v = v_swbm.min()
max_v = v_swbm.max()
max_abs = max(abs(min_v), abs(max_v))

print(f"Min Vertical SWBM: {min_v}")
print(f"Max Vertical SWBM: {max_v}")
print(f"Max Abs: {max_abs}")
