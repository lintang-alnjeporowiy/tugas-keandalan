import pandas as pd

df = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']

print("List of parts:")
for part in df['Nama Bagian'].unique():
    print(f"'{part}'")
