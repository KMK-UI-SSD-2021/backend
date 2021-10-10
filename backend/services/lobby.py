from typing import Optional

from backend.models.auth import User
from backend.models.lobby import Lobby, LobbyInRequest
from backend.models.statistics import Statistics
from backend.repositories.lobby_repository import LobbyRepository
from backend.repositories.statistics_repository import StatisticsRepository


def create_lobby(user: User,
                 statistics_repo: StatisticsRepository,
                 lobby_repo: LobbyRepository,
                 lobby_in_request: LobbyInRequest) -> int:
    lobby = Lobby(owner=user.username, **lobby_in_request.dict())
    lobby_id = lobby_repo._add(lobby)
    create_statistics(statistics_repo, lobby_id, lobby)
    return lobby_id


def create_statistics(statistics_repo: StatisticsRepository, lobby_id: int, lobby: Lobby):
    statistics = Statistics.get_default(lobby_id, lobby)
    statistics_repo._add(statistics)


def get_lobby(user: User,
              lobby_repo: LobbyRepository,
              lobby_id: int) -> Optional[Lobby]:
    if lobby := lobby_repo.get(lobby_id):
        if lobby.owner == user.username:
            return lobby
