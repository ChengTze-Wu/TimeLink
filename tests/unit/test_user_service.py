import pytest
from web_api.repositories.user_repository import UserRepository
from web_api.services.user_service import UserService

class MockUserRepository:
    @staticmethod
    def create_new_user(self, new_user_data: dict):
        username = new_user_data.get("username")
        
        return {"username": username, "password": "testpass"}

@pytest.fixture
def mock_user_repository(monkeypatch):
    monkeypatch.setattr(UserRepository, "create_new_user", MockUserRepository.create_new_user)

def test_create_user(mock_user_repository):
    user_service = UserService()
    user_data = {"username": "testuser", "password": "testpass"}
    result = user_service.create(user_data)
    assert result == {"username": "testuser", "password": "testpass"}