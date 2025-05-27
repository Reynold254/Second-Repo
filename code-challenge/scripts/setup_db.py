import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import get_connection

def setup_db():
    # Load schema.sql
    with open("lib/db/schema.sql", "r") as f:
        schema = f.read()

    # Connect to the database and execute schema
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

    print("Database setup complete!")

if __name__ == "__main__":
    setup_db()
