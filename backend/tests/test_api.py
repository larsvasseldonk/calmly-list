def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo(client):
    response = client.post(
        "/todos",
        json={"text": "Test todo"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test todo"
    assert "id" in data
    assert "createdAt" in data
    assert data["completed"] is False

def test_get_todos_with_data(client):
    client.post("/todos", json={"text": "Todo 1"})
    client.post("/todos", json={"text": "Todo 2"})
    
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_todo(client):
    # Create a todo
    create_response = client.post("/todos", json={"text": "Original text"})
    todo_id = create_response.json()["id"]
    
    # Update it
    response = client.patch(
        f"/todos/{todo_id}",
        json={"text": "Updated text", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Updated text"
    assert data["completed"] is True
    
    # Verify persistence
    get_response = client.get("/todos")
    assert get_response.json()[0]["text"] == "Updated text"

def test_delete_todo(client):
    # Create a todo
    create_response = client.post("/todos", json={"text": "To delete"})
    todo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get("/todos")
    assert len(get_response.json()) == 0

def test_delete_completed_todos(client):
    # Create todos
    client.post("/todos", json={"text": "Active 1"})
    
    create_response = client.post("/todos", json={"text": "Completed 1"})
    todo_id = create_response.json()["id"]
    client.patch(f"/todos/{todo_id}", json={"completed": True})
    
    # Delete completed
    response = client.delete("/todos/completed")
    assert response.status_code == 204
    
    # Verify only active remains
    get_response = client.get("/todos")
    todos = get_response.json()
    assert len(todos) == 1
    assert todos[0]["text"] == "Active 1"
