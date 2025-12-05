def create_test_user(client):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    return response.json()

def get_auth_token(client):
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_register_and_login(client):
    create_test_user(client)
    token = get_auth_token(client)
    assert token is not None

def test_get_todos_empty(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/todos",
        json={"text": "Test todo"},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test todo"
    assert "id" in data
    assert "createdAt" in data
    assert data["completed"] is False

def test_get_todos_with_data(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/todos", json={"text": "Todo 1"}, headers=headers)
    client.post("/todos", json={"text": "Todo 2"}, headers=headers)
    
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_todo(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a todo
    create_response = client.post("/todos", json={"text": "Original text"}, headers=headers)
    todo_id = create_response.json()["id"]
    
    # Update it
    response = client.patch(
        f"/todos/{todo_id}",
        json={"text": "Updated text", "completed": True},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Updated text"
    assert data["completed"] is True
    
    # Verify persistence
    get_response = client.get("/todos", headers=headers)
    assert get_response.json()[0]["text"] == "Updated text"

def test_delete_todo(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a todo
    create_response = client.post("/todos", json={"text": "To delete"}, headers=headers)
    todo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get("/todos", headers=headers)
    assert len(get_response.json()) == 0

def test_delete_completed_todos(client):
    create_test_user(client)
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create todos
    client.post("/todos", json={"text": "Active 1"}, headers=headers)
    
    create_response = client.post("/todos", json={"text": "Completed 1"}, headers=headers)
    todo_id = create_response.json()["id"]
    client.patch(f"/todos/{todo_id}", json={"completed": True}, headers=headers)
    
    # Delete completed
    response = client.delete("/todos/completed", headers=headers)
    assert response.status_code == 204
    
    # Verify only active remains
    get_response = client.get("/todos", headers=headers)
    todos = get_response.json()
    assert len(todos) == 1
    assert todos[0]["text"] == "Active 1"
