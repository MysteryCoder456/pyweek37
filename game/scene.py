from abc import abstractmethod, ABC
from pygame import Event, Surface


class Scene(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def on_enter(self) -> None: ...

    @abstractmethod
    def on_event(self, event: Event) -> None: ...

    @abstractmethod
    def on_update(self, dt: float) -> None: ...

    @abstractmethod
    def on_draw(self, window: Surface) -> None: ...
