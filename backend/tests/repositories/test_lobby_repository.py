import pytest

from backend.models.lobby import Lobby, Settings
from backend.repositories.lobby_repository import LobbyRepository


@pytest.fixture
def mock_lobby(mock_settings: Settings) -> Lobby:
    return Lobby(owner='test', name='test', settings=mock_settings)


class TestLobbyRepository:

    def test_add(self, mock_lobby_repo: LobbyRepository, mock_lobby: Lobby):
        mock_lobby_repo._add(lobby=mock_lobby)

    def test_get(self, mock_lobby_repo: LobbyRepository, mock_lobby: Lobby):
        lobby_id = mock_lobby_repo._add(mock_lobby)
        lobby = mock_lobby_repo.get(lobby_id=lobby_id)
        assert lobby == mock_lobby

    def test_get_not_exists(self, mock_lobby_repo: LobbyRepository):
        lobby = mock_lobby_repo.get(lobby_id=1)
        assert lobby is None
