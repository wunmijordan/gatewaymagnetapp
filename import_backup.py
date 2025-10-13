import os
os.system(f'psql "{os.environ["DATABASE_URL"]}" < backup.sql')
