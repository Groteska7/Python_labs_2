from enum import Enum
from abc import ABC, abstractmethod
from typing import List


class Manageable(ABC):
    @abstractmethod
    def set_maintenance(self) -> None:
        pass


class Diagnosable(ABC):
    @abstractmethod
    def get_detailed_report(self) -> str:
        pass


class ICloudSync(ABC):
    @abstractmethod
    def sync(self) -> None:
        pass


class ServiceStatus(Enum):
    IDLE: str = "idle"
    WORKING: str = "working"
    ERROR: str = "error"
    MAINTENANCE: str = "maintenance"


class Sersev(Manageable, Diagnosable):
    VERSION: str = "1.0.5"

    def __init__(self, name: str, max_tasks: int = 10) -> None:
        self._name: str = self._validate_name(name)
        self._max_tasks: int = self._validate_max_tasks(max_tasks)
        self._tasks: List[str] = []
        self._status: ServiceStatus = ServiceStatus.IDLE

    def _validate_name(self, name: str) -> str:
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        return name.strip()

    def _validate_max_tasks(self, limit: int) -> int:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Max tasks must be a positive integer")
        return limit

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> str:
        return self._status.value

    @property
    def load_percentage(self) -> float:
        return (len(self._tasks) / self._max_tasks) * 100

    @property
    def max_tasks(self) -> int:
        return self._max_tasks

    @max_tasks.setter
    def max_tasks(self, value: int) -> None:
        new_limit: int = self._validate_max_tasks(value)
        if new_limit < len(self._tasks):
            raise ValueError("New limit is less than current task count!")
        self._max_tasks = new_limit

    def add_task(self, task_name: str) -> None:
        if self._status == ServiceStatus.ERROR:
            raise RuntimeError("Cannot add task: service is in ERROR state")
        if len(self._tasks) >= self._max_tasks:
            self._status = ServiceStatus.ERROR
            raise OverflowError(f"Service '{self._name}' is full!")
        self._tasks.append(task_name)
        self._status = ServiceStatus.WORKING

    def clear_tasks(self) -> None:
        self._tasks.clear()
        self._status = ServiceStatus.IDLE

    def set_maintenance(self) -> None:
        self._status = ServiceStatus.MAINTENANCE

    def get_detailed_report(self) -> str:
        return self.info()

    def display(self) -> str:
        return str(self)

    def score(self) -> float:
        return self.load_percentage

    def __str__(self) -> str:
        return f"Server '{self._name}' [{self._status.value}]. Load: {len(self._tasks)}/{self._max_tasks}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sersev):
            return False
        return self._name == other._name and self._max_tasks == other._max_tasks

    def info(self) -> str:
        task_col: str = "\n".join(self._tasks)
        return f"Name: {self._name}\nTasks:\n{task_col}"