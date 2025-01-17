from models import Equipment

class EquipmentService:
    def __init__(self, repository):
        self.repository = repository

    def list_equipment(self):
        return self.repository.get_all()

    def get_equipment(self, item_id: int):
        return self.repository.get_by_id(item_id)

    def create_equipment(
        self,
        name: str,
        description: str = "",
        status: str = "available",
        location: str = "warehouse",
        condition: str = "new"
    ):
        allowed_conditions = ["new", "used", "damaged"]
        if condition not in allowed_conditions:
            raise ValueError(
                f"condition '{condition}' nie jest dozwolone. "
                f"Dozwolone wartości: {allowed_conditions}"
            )

        new_item = Equipment(
            name=name,
            description=description,
            status=status,
            location=location,
            condition=condition
        )
        return self.repository.add(new_item)

    def update_equipment(self, item_id: int, **kwargs):
        item = self.repository.get_by_id(item_id)
        if not item:
            return None

        allowed_conditions = ["new", "used", "damaged"]
        if 'condition' in kwargs:
            if kwargs['condition'] not in allowed_conditions:
                raise ValueError(
                    f"condition '{kwargs['condition']}' nie jest dozwolone. "
                    f"Dozwolone wartości: {allowed_conditions}"
                )

        for key, value in kwargs.items():
            setattr(item, key, value)

        return self.repository.update(item)

    def delete_equipment(self, item_id: int):
        item = self.repository.get_by_id(item_id)
        if not item:
            return False
        self.repository.delete(item)
        return True
