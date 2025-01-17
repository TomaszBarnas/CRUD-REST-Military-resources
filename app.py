from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from repositories.equipment_repository import EquipmentRepository
from services.equipment_service import EquipmentService
from controllers.equipment_controller import init_equipment_controller

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Database configuration: SQLite with SQLAlchemy ORM
    engine = create_engine('sqlite:///equipment.db', echo=False)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    db_session = Session()

    # Initialize repository and service layer
    equipment_repo = EquipmentRepository(db_session)
    equipment_service = EquipmentService(equipment_repo)

    # Register RESTful API endpoints via blueprint
    init_equipment_controller(app, equipment_service)

    # Route to serve the main page
    @app.route("/")
    def home():
        """
        Serves the main HTML page for the application.
        """
        return render_template("index.html")

    return app

if __name__ == "__main__":
    # Create and run the Flask application
    app = create_app()
    app.run(debug=True)
