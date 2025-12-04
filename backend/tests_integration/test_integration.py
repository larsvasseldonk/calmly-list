def test_integration_lifecycle(client):
    """
    Full integration test of the Todo lifecycle:
    Create -> Read -> Update -> Delete
    """
    # 1. Create a Todo
    todo_data = {
        "text": "Integration Test Todo",
        "priority": "high",
        "category": "testing"
    }
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    created_todo = response.json()
    assert created_todo["text"] == todo_data["text"]
    assert created_todo["priority"] == todo_data["priority"]
    assert created_todo["completed"] is False
    todo_id = created_todo["id"]

    # 2. Read All Todos
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["id"] == todo_id

    # 3. Update Todo
    update_data = {
        "text": "Updated Integration Todo",
        "completed": True
    }
    response = client.patch(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["text"] == update_data["text"]
    assert updated_todo["completed"] is True
    
    # Verify update persisted
    response = client.get(f"/todos")
    todos = response.json()
    assert todos[0]["text"] == update_data["text"]
    assert todos[0]["completed"] is True

    # 4. Delete Todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_delete_completed_integration(client):
    """Integration test for deleting completed todos"""
    # Create active todo
    client.post("/todos", json={"text": "Active Todo"})
    
    # Create completed todo
    response = client.post("/todos", json={"text": "Completed Todo"})
    todo_id = response.json()["id"]
    client.patch(f"/todos/{todo_id}", json={"completed": True})
    
    # Verify we have 2 todos
    response = client.get("/todos")
    assert len(response.json()) == 2
    
    # Delete completed
    response = client.delete("/todos/completed")
    assert response.status_code == 204
    
    # Verify only active remains
    response = client.get("/todos")
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["text"] == "Active Todo"
