from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Define the base class for ORM models
Base = declarative_base()

class Equipment(Base):
    """
    Represents a piece of equipment in the inventory system.
    """
    __tablename__ = 'equipment'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for the equipment
    name = Column(String, nullable=False)  # Name of the equipment (required)
    description = Column(String)  # Optional description of the equipment
    status = Column(String, default="available")  # Status of the equipment (e.g., available, in use)

    # Additional fields for more detailed information
    location = Column(String, default="warehouse")  # Location of the equipment
    condition = Column(String, default="new")  # Condition of the equipment (e.g., new, used, damaged)
