with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'r') as f:
    content = f.read()

# Replace old load calculation with absolute wave bending moment first
old_str = "vbm_total = df_wbm['Momen Vertikal (N.m)'] + max_abs_swbm_v"
new_str = "vbm_total = np.abs(df_wbm['Momen Vertikal (N.m)']) + max_abs_swbm_v"

if old_str in content:
    content = content.replace(old_str, new_str)
    print("Successfully replaced with absolute load formula!")
else:
    print("Target formula string not found!")

# Also make sure there are no other places where raw df_wbm['Momen Vertikal (N.m)'] is used without abs
# (Let's check if there are other occurrences)

with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'w') as f:
    f.write(content)
