from flask import Blueprint, request, jsonify

# Create a blueprint for the equipment endpoints
equipment_bp = Blueprint('equipment_bp', __name__)

def init_equipment_controller(app, equipment_service):
    """
    Initializes the equipment-related endpoints and registers them with the Flask app.

    :param app: The Flask application instance.
    :param equipment_service: The service layer handling business logic for equipment.
    """

    @equipment_bp.route('/equipment', methods=['GET'])
    def get_all_equipment():
        """
        Retrieves all equipment entries.

        :return: JSON list of all equipment with a 200 status code.
        """
        all_items = equipment_service.list_equipment()
        return jsonify([
            {
                "id": i.id,
                "name": i.name,
                "description": i.description,
                "status": i.status,
                "location": i.location,
                "condition": i.condition
            } for i in all_items
        ]), 200

    @equipment_bp.route('/equipment/<int:item_id>', methods=['GET'])
    def get_equipment(item_id):
        """
        Retrieves a specific equipment entry by ID.

        :param item_id: The ID of the equipment to retrieve.
        :return: JSON object of the equipment if found, otherwise a 404 error.
        """
        item = equipment_service.get_equipment(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404
        return jsonify({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "status": item.status,
            "location": item.location,
            "condition": item.condition
        }), 200

    @equipment_bp.route('/equipment', methods=['POST'])
    def create_equipment():
        """
        Creates a new equipment entry.

        :return: JSON object of the newly created equipment with a 201 status code.
                 Returns a 400 error if validation fails.
        """
        data = request.json
        try:
            new_item = equipment_service.create_equipment(
                name=data.get("name"),
                description=data.get("description", ""),
                status=data.get("status", "available"),
                location=data.get("location", "warehouse"),
                condition=data.get("condition", "new")
            )
            return jsonify({
                "id": new_item.id,
                "name": new_item.name,
                "description": new_item.description,
                "status": new_item.status,
                "location": new_item.location,
                "condition": new_item.condition
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @equipment_bp.route('/equipment/<int:item_id>', methods=['PUT'])
    def update_equipment(item_id):
        """
        Updates an existing equipment entry.

        :param item_id: The ID of the equipment to update.
        :return: JSON object of the updated equipment with a 200 status code,
                 or a 404 error if the equipment is not found.
        """
        data = request.json
        try:
            updated_item = equipment_service.update_equipment(item_id, **data)
            if not updated_item:
                return jsonify({"message": "Item not found"}), 404

            return jsonify({
                "id": updated_item.id,
                "name": updated_item.name,
                "description": updated_item.description,
                "status": updated_item.status,
                "location": updated_item.location,
                "condition": updated_item.condition
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @equipment_bp.route('/equipment/<int:item_id>', methods=['DELETE'])
    def delete_equipment(item_id):
        """
        Deletes an equipment entry by ID.

        :param item_id: The ID of the equipment to delete.
        :return: A success message with a 200 status code, or a 404 error if not found.
        """
        result = equipment_service.delete_equipment(item_id)
        if not result:
            return jsonify({"message": "Item not found"}), 404
        return jsonify({"message": "Item deleted"}), 200

    # Register the blueprint with the Flask application
    app.register_blueprint(equipment_bp, url_prefix='/api')
