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

def test_login_invalid_email(client):
    """Test login with invalid email"""
    create_test_user(client)
    response = client.post(
        "/login",
        data={"username": "wrong@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_invalid_password(client):
    """Test login with invalid password"""
    create_test_user(client)
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_register_duplicate_email(client):
    """Test that registering with duplicate email fails"""
    create_test_user(client)
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_access_todos_without_token(client):
    """Test that accessing protected route without token fails"""
    response = client.get("/todos")
    assert response.status_code == 401


def test_access_todos_with_invalid_token(client):
    """Test that accessing protected route with invalid token fails"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/todos", headers=headers)
    assert response.status_code == 401


def test_create_todo_without_token(client):
    """Test that creating todo without token fails"""
    response = client.post("/todos", json={"text": "Test todo"})
    assert response.status_code == 401


def test_token_isolation_between_users(client):
    """Test that users can only access their own todos"""
    # Create first user
    create_test_user(client)
    token1 = get_auth_token(client)
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    # Create second user
    response = client.post(
        "/register",
        json={"email": "user2@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    
    response = client.post(
        "/login",
        data={"username": "user2@example.com", "password": "password123"}
    )
    token2 = response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User 1 creates a todo
    client.post("/todos", json={"text": "User 1 todo"}, headers=headers1)
    
    # User 2 creates a todo
    client.post("/todos", json={"text": "User 2 todo"}, headers=headers2)
    
    # User 1 should only see their todo
    response = client.get("/todos", headers=headers1)
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["text"] == "User 1 todo"
    
    # User 2 should only see their todo
    response = client.get("/todos", headers=headers2)
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["text"] == "User 2 todo"
