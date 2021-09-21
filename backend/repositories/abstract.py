from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def _add(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def _add_bulk(self, *args, **kwargs) -> None:
        raise NotImplementedError
