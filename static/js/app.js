document.addEventListener('DOMContentLoaded', () => {
    // Fetch and render the equipment list on page load
    fetchEquipmentList();
  
    // Handle the submission of the "Add Equipment" form
    const form = document.getElementById('newEquipmentForm');
    form.addEventListener('submit', event => {
      event.preventDefault(); // Prevent page reload on form submission
  
      // Collect form input values
      const name = document.getElementById('equipName').value;
      const description = document.getElementById('equipDesc').value;
      const status = document.getElementById('equipStatus').value;
      const location = document.getElementById('equipLocation').value;
      const condition = document.getElementById('equipCondition').value;
  
      // Send a POST request to create a new equipment entry
      fetch('/api/equipment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description, status, location, condition })
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(data.error || 'Error adding equipment');
            });
          }
          return response.json();
        })
        .then(newItem => {
          console.log('New equipment added:', newItem);
          fetchEquipmentList(); // Refresh the equipment list
          form.reset(); // Clear the form
        })
        .catch(err => {
          alert('Error: ' + err.message);
          console.error(err);
        });
    });
  });
  
  /**
   * Fetches the list of equipment from the API and renders it in the table.
   */
  function fetchEquipmentList() {
    fetch('/api/equipment')
      .then(response => response.json())
      .then(data => {
        console.log('Equipment list:', data);
        renderEquipmentTable(data); // Populate the table with data
      })
      .catch(err => {
        console.error('Error fetching equipment:', err);
      });
  }
  
  /**
   * Renders the equipment data as rows in the HTML table.
   * 
   * @param {Array} equipmentList - List of equipment objects.
   */
  function renderEquipmentTable(equipmentList) {
    const tableBody = document.querySelector('#equipmentTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows
  
    equipmentList.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.name}</td>
        <td>${item.description}</td>
        <td>${item.status}</td>
        <td>${item.location}</td>
        <td>${item.condition}</td>
        <td>
          <button class="btn btn-sm btn-info" onclick="editItem(${item.id})">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">Delete</button>
        </td>
      `;
      tableBody.appendChild(row);
    });
  }
  
  /**
   * Deletes an equipment item by ID.
   * 
   * @param {number} id - The ID of the equipment to delete.
   */
  function deleteItem(id) {
    if (!confirm(`Are you sure you want to delete item #${id}?`)) {
      return;
    }
  
    fetch(`/api/equipment/${id}`, { method: 'DELETE' })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Error deleting equipment');
          });
        }
        return response.json();
      })
      .then(res => {
        alert(res.message); // Notify the user about the deletion
        fetchEquipmentList(); // Refresh the list
      })
      .catch(err => {
        alert('Error: ' + err.message);
        console.error(err);
      });
  }
  
  /**
   * Fetches the details of an equipment item and populates the edit modal.
   * 
   * @param {number} id - The ID of the equipment to edit.
   */
  function editItem(id) {
    fetch(`/api/equipment/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Item not found');
        }
        return response.json();
      })
      .then(item => {
        // Populate the modal form with equipment details
        document.getElementById('editId').value = item.id;
        document.getElementById('editName').value = item.name;
        document.getElementById('editDesc').value = item.description;
        document.getElementById('editStatus').value = item.status;
        document.getElementById('editLocation').value = item.location;
        document.getElementById('editCondition').value = item.condition;
  
        // Display the modal
        const editModal = new bootstrap.Modal(document.getElementById('editModal'));
        editModal.show();
      })
      .catch(err => {
        alert(err.message);
        console.error(err);
      });
  }
  
  /**
   * Saves the changes made in the edit modal.
   */
  function saveEdit() {
    const id = document.getElementById('editId').value;
    const name = document.getElementById('editName').value;
    const description = document.getElementById('editDesc').value;
    const status = document.getElementById('editStatus').value;
    const location = document.getElementById('editLocation').value;
    const condition = document.getElementById('editCondition').value;
  
    fetch(`/api/equipment/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description, status, location, condition })
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.error || 'Error updating equipment');
          });
        }
        return response.json();
      })
      .then(updatedItem => {
        console.log('Updated item:', updatedItem);
        fetchEquipmentList(); // Refresh the equipment list
  
        // Close the modal
        const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
        editModal.hide();
      })
      .catch(err => {
        alert('Error: ' + err.message);
        console.error(err);
      });
  }
  