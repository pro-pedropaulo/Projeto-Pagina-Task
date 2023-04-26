import os
import importlib
from database import connect

migrations_folder = 'migrations'

def get_migration_files():
    migration_files = [f for f in os.listdir(migrations_folder) if f.endswith('.py')]
    migration_files.sort()
    return migration_files

def run_migrations():
    conn = connect()
    migration_files = get_migration_files()

    for migration_file in migration_files:
        migration_name = migration_file[:-3]
        migration_module = importlib.import_module(f'{migrations_folder}.{migration_name}')
        print(f'Running migration: {migration_name}')
        migration_module.up(conn)

    conn.close()

if __name__ == "__main__":
    run_migrations()
