from src.database.db import engine
from src.database.base import BaseEntity

# Import all entities so SQLAlchemy knows about them!
import src.entities

print("Creating all database tables in Supabase...")
BaseEntity.metadata.create_all(bind=engine)
print("Tables created successfully!")

print("\nStarting data seeding...")
import src.seed_company_data
print("Data seeding complete!")
