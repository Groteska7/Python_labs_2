from typing import TypeVar, Generic, Callable, Optional, List, Protocol, Self


class Displayable(Protocol):
    def display(self) -> str:
        ...


class Scorable(Protocol):
    def score(self) -> float:
        ...


D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
T = TypeVar('T')
R = TypeVar('R')


class TypedCollection(Generic[T]):
    def __init__(self, name: str = "") -> None:
        self._items: List[T] = []
        self._name: str = name

    def add(self, item: T) -> Self:
        self._items.append(item)
        return self

    def remove(self, item: T) -> Self:
        self._items.remove(item)
        return self

    def get_all(self) -> List[T]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: Optional[int] = None) -> T | List[T]:
        if index is None:
            return list(self._items)
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def find_by_name(self, name: str) -> Optional[T]:
        for item in self._items:
            if hasattr(item, 'name') and item.name == name:
                return item
        return None

    def find_by_index(self, index: int) -> Optional[T]:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def remove_by_name(self, name: str) -> None:
        self._items = [item for item in self._items
                       if not (hasattr(item, 'name') and item.name == name)]

    def remove_by_index(self, index: int) -> None:
        if 0 <= index < len(self._items):
            self._items.pop(index)

    def get_only_type(self, kind: type) -> List[T]:
        return [obj for obj in self._items if isinstance(obj, kind)]

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]

    def __str__(self) -> str:
        return f"TypedCollection(name='{self._name}', count={len(self._items)})"

    def __repr__(self) -> str:
        return self.__str__()