import pandas as pd

df_scant = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantlling_rapi.csv', sep=';')
df_scant.columns = ['Nama Bagian', 'n', 'b', 'h', 'a', 'Z']

# Load cor-rate
df_cor = pd.read_csv('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/cor-rate.csv')
print("Corrosion rates:")
print(df_cor)

# Define mapping function
def map_element(name):
    name_lower = name.lower()
    
    # Bottom plate
    if 'pelat bottom' in name_lower or 'chine luar' in name_lower:
        return 'OPB'
    # Bottom stiffeners (Web and Frame/Flange)
    elif 'long stiff bottom' in name_lower or 'pembujur' in name_lower:
        if 'web' in name_lower:
            return 'SBW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SBF'
        else:
            # Default to web
            return 'SBW'
    # Inner bottom plate
    elif 'hopper dalam' in name_lower or 'inner bottom' in name_lower:
        return 'IPB'
    # Deck plate
    elif 'pelat deck' in name_lower:
        return 'DP'
    # Deck stiffeners (Web and Frame/Flange)
    elif 'long stiff deck' in name_lower:
        if 'web' in name_lower:
            return 'DPW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'DPF'
        else:
            return 'DPW'
    # Bulkhead (Sekat)
    elif 'sekat memanjang' in name_lower or 'sekat' in name_lower:
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'SLW'
    # Side shell plate
    elif 'pelat sisi' in name_lower:
        return 'OPB' # Or DP, let's check. Standard is outer plate OPB.
    # Side shell stiffeners or other generic stiffeners
    elif 'long stiff side shell' in name_lower or 'long stiff web' in name_lower or 'long stiff cl' in name_lower:
        # Side shell and other internal longitudinals can map to Sekat Long Web/Flange
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'SLW'
    else:
        # Default fallback
        if 'web' in name_lower:
            return 'SLW'
        elif 'frame' in name_lower or 'flange' in name_lower:
            return 'SLF'
        else:
            return 'OPB'

df_scant['mapped_index'] = df_scant['Nama Bagian'].apply(map_element)
df_scant = df_scant.merge(df_cor, left_on='mapped_index', right_on='index', how='left')

missing = df_scant[df_scant['μ (a) [mm/years]'].isna()]
print(f"Missing mappings: {len(missing)}")
if len(missing) > 0:
    print(missing['Nama Bagian'].unique())
else:
    print("All elements successfully mapped!")
    print(df_scant[['Nama Bagian', 'mapped_index', 'μ (a) [mm/years]']].head(20))
    print(df_scant[['Nama Bagian', 'mapped_index', 'μ (a) [mm/years]']].tail(20))
