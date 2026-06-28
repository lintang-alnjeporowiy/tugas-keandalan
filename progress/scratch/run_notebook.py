import json
import traceback
import matplotlib
matplotlib.use('Agg') # Non-interactive backend to prevent blocking

with open('/mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/main.ipynb') as f:
    nb = json.load(f)

# Global execution context
exec_globals = {
    'display': lambda x: print(x)
}

print("Executing code cells in main.ipynb with Agg backend...")
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        print(f"\n--- Running Cell {i} (id: {cell['id']}) ---")
        code = ''.join(cell['source'])
        try:
            exec(code, exec_globals)
        except Exception as e:
            print(f"Error in Cell {i}:")
            traceback.print_exc()
            exit(1)

print("\nAll cells executed successfully!")
