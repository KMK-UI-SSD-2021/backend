from pydantic import BaseModel

from backend.models.common import Tag
from backend.models.lobby import Lobby

Image = str
ImageTagsCounts = dict[Image, dict[Tag, int]]


class UserChoices(BaseModel):
    choices: dict[Image, Tag]


class Statistics(BaseModel):
    lobby_id: int
    times_gathered: int = 0
    image_tags_counts: ImageTagsCounts

    @staticmethod
    def get_default(lobby_id: int, lobby: Lobby):
        tags_counts: dict[Tag, int] = {}
        for tag in lobby.settings.tags:
            tags_counts[tag] = 0

        image_tags_counts: ImageTagsCounts = {}
        for image in lobby.settings.images:
            image_tags_counts[image.url] = tags_counts.copy()

        return Statistics(lobby_id=lobby_id,
                          times_gathered=0,
                          image_tags_counts=image_tags_counts)
