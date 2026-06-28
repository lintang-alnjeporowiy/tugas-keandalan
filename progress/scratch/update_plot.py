with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'r') as f:
    content = f.read()

# Replace the subplot layout
old_str = 'fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))'
new_str = 'fig, axes = plt.subplots(2, 1, figsize=(14, 10))'

if old_str in content:
    content = content.replace(old_str, new_str)
    print("Successfully replaced layout!")
else:
    print("Target string not found!")

with open('/home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py', 'w') as f:
    f.write(content)
