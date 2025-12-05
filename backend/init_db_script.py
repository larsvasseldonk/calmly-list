from app.database import init_db
from app.schema import User, TodoModel

print("Initializing database...")
init_db()
print("Database initialized.")
