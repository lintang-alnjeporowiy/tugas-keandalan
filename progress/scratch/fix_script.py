with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'r') as f:
    content = f.read()

# Replace the broken lines
target = '''     "ax.set_xlabel('Ship Age (years)', fontsize=10)\\n",
    "    \\"ax.set_ylabel(r'Safety Index ($\\\\\\\\beta$)', fontsize=10)\\\\n\\",\\n",
    "    \\"ax.set_title(r'Safety Index ($\\\\\\\\beta$) vs Ship Age')\\\\n\\",\\n"
     "ax.set_xticks(ages)\\n",'''

# Let's search by locating:
# "ax.set_xlabel('Ship Age (years)', fontsize=10)\n",
# and replacing the next two lines
lines = content.split('\n')
for i, line in enumerate(lines):
    if "ax.set_xlabel('Ship Age (years)', fontsize=10)" in line:
        print(f"Found line at index {i}: {line}")
        print(f"Next line: {lines[i+1]}")
        print(f"Next next line: {lines[i+2]}")
        
        # Replace lines i+1 and i+2
        lines[i+1] = '     "ax.set_ylabel(r\'Safety Index ($\\\\beta$)\', fontsize=10)\\n",'
        lines[i+2] = '     "ax.set_title(r\'Safety Index ($\\\\beta$) vs Ship Age\')\\n",'

with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'w') as f:
    f.write('\n'.join(lines))

print("Modified generate_notebook.py successfully!")
