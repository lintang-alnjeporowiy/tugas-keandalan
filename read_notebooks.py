import json

print("="*60)
print("SECTION_MODULUS.IPYNB")
print("="*60)
nb = json.load(open('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/section_modulus.ipynb'))
cells = nb['cells']
for i, c in enumerate(cells):
    print(f"\n--- Cell {i} ({c['cell_type']}) ---")
    src = ''.join(c['source'])
    print(src)
