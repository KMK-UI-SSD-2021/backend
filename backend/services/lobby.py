from typing import Optional

from backend.models.auth import User
from backend.models.lobby import Lobby, LobbyInRequest
from backend.repositories.lobby_repository import LobbyRepository


def create_lobby(user: User,
                 lobby_repo: LobbyRepository,
                 lobby_in_request: LobbyInRequest) -> int:
    lobby = Lobby(owner=user.username, **lobby_in_request.dict())
    return lobby_repo._add(lobby)


def get_lobby(user: User,
              lobby_repo: LobbyRepository,
              lobby_id: int) -> Optional[Lobby]:
    if lobby := lobby_repo.get(lobby_id):
        if lobby.owner == user.username:
            return lobby
