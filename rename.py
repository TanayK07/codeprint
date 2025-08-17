# fix_toml.py
import re

# Read the file
with open('pyproject.toml', 'r') as f:
    lines = f.readlines()

# Find and fix duplicate keys
seen_keys = set()
fixed_lines = []
in_table = None

for i, line in enumerate(lines, 1):
    # Check for table headers
    if line.strip().startswith('['):
        in_table = line.strip()
        seen_keys = set()
    
    # Check for key-value pairs
    if '=' in line and not line.strip().startswith('#'):
        key = line.split('=')[0].strip()
        if key in seen_keys:
            print(f"Found duplicate at line {i}: {key}")
            continue  # Skip duplicate
        seen_keys.add(key)
    
    fixed_lines.append(line)

# Write back
with open('pyproject.toml', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Fixed pyproject.toml")