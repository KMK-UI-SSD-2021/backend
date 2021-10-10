import pytest
from starlette.testclient import TestClient

from backend.models.auth import UserInRequest
from backend.models.lobby import LobbyInRequest, Settings
from backend.models.statistics import UserChoices
from backend.services.auth import create_user
from backend.services.lobby import create_lobby


@pytest.fixture
def mock_user() -> UserInRequest:
    return UserInRequest(username='test', password='test')


@pytest.fixture
def mock_lobby(mock_settings: Settings) -> LobbyInRequest:
    return LobbyInRequest(name='test', settings=mock_settings)


@pytest.fixture
def mock_user_choices() -> UserChoices:
    return UserChoices(choices={
        'https://imgur.com/1': 'test1',
        'https://imgur.com/2': 'test2'
    })


class TestRegister:

    def test_register_new_user(self, mock_client: TestClient, mock_user: UserInRequest):
        response = mock_client.post('/api/v1/register', json=mock_user.dict())
        json_response = response.json()

        assert 'token' in json_response
        assert len(json_response['token']) == 64

    def test_register_user_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        create_user(mock_client.app.state.user_repo, mock_user.username, mock_user.password)

        response = mock_client.post('/api/v1/register', json=mock_user.dict())
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'user exists'


class TestLogin:

    def test_login_user_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        create_user(mock_client.app.state.user_repo, mock_user.username, mock_user.password)

        response = mock_client.post('/api/v1/login', json=mock_user.dict())
        json_response = response.json()

        assert 'token' in json_response
        assert len(json_response['token']) == 64

    def test_login_not_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        response = mock_client.post('/api/v1/login', json=mock_user.dict())
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'wrong credentials'


class TestCreateLobby:

    def test_create_lobby_authorized(self,
                                     mock_client: TestClient,
                                     mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        token = create_user(repo=user_repo, username='test', password='test')

        response = mock_client.post('/api/v1/lobby',
                                    headers={'token': token},
                                    json=mock_lobby.dict())
        json_response = response.json()

        assert 'lobby_id' in json_response
        assert json_response['lobby_id'] == 1

    def test_create_lobby_unauthorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        response = mock_client.post('/api/v1/lobby', json=mock_lobby.dict())
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'


class TestGetLobby:

    def test_get_lobby_authorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')
        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/lobby/{lobby_id}',
                                   headers={'token': token})
        json_response = response.json()

        assert json_response == {
            'owner': 'test',
            'name': mock_lobby.name,
            'settings': mock_lobby.settings
        }

    def test_get_lobby_wrong_token(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')

        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/lobby/{lobby_id}',
                                   headers={'token': 'bad token'})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'

    def test_get_lobby_wrong_user(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token_owner = create_user(repo=user_repo, username='test', password='test')
        token_random = create_user(repo=user_repo, username='random', password='random')

        lobby_id = create_lobby(user_repo.get_user_by_token(token_owner), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/lobby/{lobby_id}',
                                   headers={'token': token_random})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'not found'

    def test_get_lobby_unauthorized(self, mock_client: TestClient):
        response = mock_client.get('/api/v1/lobby/1')
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'

    def test_get_lobby_not_exists(self, mock_client: TestClient):
        user_repo = mock_client.app.state.user_repo
        token = create_user(repo=user_repo, username='test', password='test')

        response = mock_client.get('/api/v1/lobby/1',
                                   headers={'token': token})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'not found'


class TestSubmitChoices:

    def test_submit_choices_authorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest,
                                       mock_user_choices: UserChoices):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')
        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.put(f'/api/v1/statistics/{lobby_id}',
                                   json=mock_user_choices.dict(),
                                   headers={'token': token})
        json_response = response.json()

        assert json_response == {
            'lobby_id': lobby_id,
            'times_gathered': 1,
            'image_tags_counts': {
                'https://imgur.com/1': {'test1': 1, 'test2': 0},
                'https://imgur.com/2': {'test1': 0, 'test2': 1}
            }
        }

    def test_submit_choices_unauthorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest,
                                         mock_user_choices: UserChoices):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')

        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.put(f'/api/v1/statistics/{lobby_id}',
                                   json=mock_user_choices.dict(),
                                   headers={'token': 'bad token'})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'

    def test_submit_choices_not_exists(self, mock_client: TestClient,
                                       mock_user_choices: UserChoices):
        user_repo = mock_client.app.state.user_repo
        token = create_user(repo=user_repo, username='test', password='test')

        response = mock_client.put('/api/v1/statistics/1',
                                   json=mock_user_choices.dict(),
                                   headers={'token': token})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'not found'


class TestGetStatistics:

    def test_get_statistics_authorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')
        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/statistics/{lobby_id}',
                                   headers={'token': token})
        json_response = response.json()

        assert json_response == {
            'lobby_id': lobby_id,
            'times_gathered': 0,
            'image_tags_counts': {
                'https://imgur.com/1': {'test1': 0, 'test2': 0},
                'https://imgur.com/2': {'test1': 0, 'test2': 0}
            }
        }

    def test_get_statistics_unauthorized(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token = create_user(repo=user_repo, username='test', password='test')

        lobby_id = create_lobby(user_repo.get_user_by_token(token), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/statistics/{lobby_id}',
                                   headers={'token': 'bad token'})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'

    def test_get_lobby_wrong_user(self, mock_client: TestClient, mock_lobby: LobbyInRequest):
        user_repo = mock_client.app.state.user_repo
        lobby_repo = mock_client.app.state.lobby_repo
        statistics_repo = mock_client.app.state.statistics_repo

        token_owner = create_user(repo=user_repo, username='test', password='test')
        token_random = create_user(repo=user_repo, username='random', password='random')

        lobby_id = create_lobby(user_repo.get_user_by_token(token_owner), statistics_repo,
                                lobby_repo, mock_lobby)

        response = mock_client.get(f'/api/v1/statistics/{lobby_id}',
                                   headers={'token': token_random})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'not found'

    def test_get_lobby_unauthorized(self, mock_client: TestClient):
        response = mock_client.get('/api/v1/statistics/1')
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'unauthorized'

    def test_get_statistics_not_exists(self, mock_client: TestClient):
        user_repo = mock_client.app.state.user_repo
        token = create_user(repo=user_repo, username='test', password='test')

        response = mock_client.get('/api/v1/statistics/1',
                                   headers={'token': token})
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'not found'
