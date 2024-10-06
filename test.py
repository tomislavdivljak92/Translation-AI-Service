import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app  # Assuming FastAPI app is created in main.py
from database import get_db  # Assuming you have Base and get_db in database.py
from crud import create_translation_task, get_translation_task
from unittest.mock import patch
from models import Base

# Use SQLite in-memory database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
print(f"Using database URL: {SQLALCHEMY_TEST_DATABASE_URL}")
# Create the SQLite in-memory database engine
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all the tables in the SQLite test database
Base.metadata.create_all(bind=engine)

# Use the override in the app
app.dependency_overrides[get_db] = override_get_db

# Initialize the FastAPI test client
client = TestClient(app)

# Test the create task and get task API
def test_create_task():
    response = client.post("/translate", json={
        "text": "Hello World",
        "languages": ["es", "fr"]  # Ensure this structure matches your API definition
    })
    
    assert response.status_code == 200
    json_data = response.json()
    assert "task_id" in json_data

    task_id = json_data["task_id"]

    # Now, test getting the task back
    response = client.get(f"/translate/{task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id

# Mocking OpenAI API calls in testing
@patch("utily.openai.ChatCompletion.create")  # Ensure this path matches your module structure
def test_openai_mock(mock_create):
    # Mock OpenAI response
    mock_create.return_value = {
        "choices": [{"message": {"content": "Translated text"}}]
    }

    db = next(override_get_db())

    # Create a translation task
    task = create_translation_task(db, "Test text", ["es"])

    # Call the function that interacts with OpenAI
    from utily import perform_translation  # Ensure this path matches your module structure
    perform_translation(task.id, "Test text", ["es"], db)

    # Check if the task is updated with mock response
    updated_task = get_translation_task(db, task.id)
    assert updated_task.translations["es"] == "Translated text"

if __name__ == "__main__":
    pytest.main()