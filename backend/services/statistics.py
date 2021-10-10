from typing import Optional

from backend.models.auth import User
from backend.models.statistics import Statistics, UserChoices
from backend.repositories.lobby_repository import LobbyRepository
from backend.repositories.statistics_repository import StatisticsRepository
from backend.services.lobby import get_lobby


def get_statistics(user: User,
                   statistics_repo: StatisticsRepository,
                   lobby_repo: LobbyRepository,
                   lobby_id: int) -> Optional[Statistics]:
    if get_lobby(user, lobby_repo, lobby_id) is not None:
        return statistics_repo.get(lobby_id)


def update_statistics(statistics_repo: StatisticsRepository,
                      statistics: Statistics,
                      choices: UserChoices) -> Statistics:
    statistics.times_gathered += 1
    for image, tag in choices.choices.items():
        assert image in statistics.image_tags_counts
        assert tag in statistics.image_tags_counts[image]
        statistics.image_tags_counts[image][tag] += 1

    statistics_repo.update(statistics)
    return statistics
