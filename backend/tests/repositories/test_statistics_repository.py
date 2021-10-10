import pytest

from backend.models.statistics import Statistics
from backend.repositories.statistics_repository import StatisticsRepository


@pytest.fixture
def mock_statistics() -> Statistics:
    return Statistics(lobby_id=1,
                      times_gathered=42,
                      image_tags_counts={
                          'https://imgur.com/1': {
                              'tag1': 12,
                              'tag2': 30,
                          },
                          'https://imgur.com/2': {
                              'tag1': 34,
                              'tag2': 6
                          },
                          'https://imgur.com/3': {
                              'tag1': 22,
                              'tag2': 20
                          }
                      })


class TestStatisticsRepository:

    def test_add(self, mock_statistics_repo: StatisticsRepository, mock_statistics: Statistics):
        mock_statistics_repo._add(mock_statistics)

    def test_get(self, mock_statistics_repo: StatisticsRepository, mock_statistics: Statistics):
        mock_statistics_repo._add(mock_statistics)
        statistics = mock_statistics_repo.get(mock_statistics.lobby_id)
        assert statistics == mock_statistics

    def test_get_not_exists(self, mock_statistics_repo: StatisticsRepository):
        statistics = mock_statistics_repo.get(lobby_id=1)
        assert statistics is None

    def test_update(self, mock_statistics_repo: StatisticsRepository, mock_statistics: Statistics):
        mock_statistics_repo._add(mock_statistics)
        mock_statistics.times_gathered = 50
        mock_statistics.image_tags_counts = {
            'https://imgur.com/1': {
                'tag1': 20,
                'tag2': 30,
            },
            'https://imgur.com/2': {
                'tag1': 34,
                'tag2': 16
            },
            'https://imgur.com/3': {
                'tag1': 25,
                'tag2': 25
            }
        }
        mock_statistics_repo.update(mock_statistics)
        statistics = mock_statistics_repo.get(mock_statistics.lobby_id)
        assert statistics == mock_statistics
