import os
import re

MIGRATIONS_DIR = 'accounts/migrations'

for filename in os.listdir(MIGRATIONS_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(MIGRATIONS_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        # Remove `upload_to=...` arguments entirely
        new_content = re.sub(r",\s*upload_to=[^),]+", "", content)

        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Patched {filename}")
