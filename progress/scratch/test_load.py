import pandas as pd
import numpy as np

# Load SWBM
df_swbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/SWBM.csv', sep=';')
print("SWBM columns:", df_swbm.columns.tolist())
print(df_swbm.describe())

# Load WBM
df_wbm = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/Wave-Bending-Moment.csv', sep=';')
print("WBM columns:", df_wbm.columns.tolist())
print(df_wbm.describe())
