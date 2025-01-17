from models import Equipment
from sqlalchemy.orm import Session

class EquipmentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self):
        return self.db_session.query(Equipment).all()

    def get_by_id(self, item_id: int):
        return self.db_session.query(Equipment).filter_by(id=item_id).first()

    def add(self, equipment: Equipment):
        self.db_session.add(equipment)
        self.db_session.commit()
        return equipment

    def delete(self, equipment: Equipment):
        self.db_session.delete(equipment)
        self.db_session.commit()

    def update(self, equipment: Equipment):
        self.db_session.commit()
        return equipment
