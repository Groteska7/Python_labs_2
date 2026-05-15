from typing import Optional
from ..lab01.model import Sersev, ServiceStatus
from ..lab02.collection import SersevList
from abc import ABC, abstractmethod


class ICloudSync(ABC):
    @abstractmethod
    def sync(self) -> None:
        pass


class ComputeServer(Sersev):
    def __init__(self, name: str, cpu_power: float = 0.5, max_tasks: int = 10) -> None:
        super().__init__(name, max_tasks)
        self._cpu_power: float = cpu_power

    @property
    def _predicted_time(self) -> float:
        return len(self._tasks) / self._cpu_power if self._cpu_power > 0 else 0.0

    def get_estimated_time(self) -> float | str:
        if self._cpu_power > 0:
            return self._predicted_time
        else:
            return "no tasks, resting!"

    def get_detailed_report(self) -> str:
        base_info: str = super().get_detailed_report()
        return f"[COMPUTE NODE]\n{base_info}\nCPU Power: {self._cpu_power}"

    def set_maintenance(self) -> None:
        print(f"Stopping computations on {self._name}...")
        super().set_maintenance()

    def display(self) -> str:
        return f"ComputeServer({self._name}, cpu={self._cpu_power})"

    def score(self) -> float:
        return self._cpu_power * 10

    def __str__(self) -> str:
        return f"Compute server {self._name} [{self._status.value}] power {self._cpu_power} tasks/sec"

    def info(self) -> str:
        task_col: str = "\n".join(self._tasks)
        return (f"Name: {self._name}\n"
                f"Status: [{self._status.value}]\n"
                f"Total power: {self._cpu_power}\n"
                f"Predicted time: {self._predicted_time} sec\n"
                f"Tasks:\n{task_col}")


class StorageServer(Sersev):
    def __init__(self, name: str, all_memory: int = 40) -> None:
        super().__init__(name)
        self._max_tasks: int = all_memory // 4
        self._all_memory: int = all_memory

    @property
    def _use_memory(self) -> int:
        return len(self._tasks) * 4

    def get_detailed_report(self) -> str:
        return f"[STORAGE NODE] {self._name}\nAvailable memory: {self._all_memory} bytes"

    def set_maintenance(self) -> None:
        print(f"Syncing file system {self._name} before maintenance...")
        super().set_maintenance()

    def sync(self) -> None:
        print(f"Cloud sync for {self._name} started...")

    def display(self) -> str:
        return f"StorageServer({self._name}, memory={self._all_memory})"

    def score(self) -> float:
        return float(self._all_memory)

    def __str__(self) -> str:
        return (f"Server with big memory {self._name} [{self._status.value}] "
                f"with {self._all_memory} bytes")

    def info(self) -> str:
        task_col: str = "\n".join(self._tasks)
        return (f"Name: {self._name}\n"
                f"Status: [{self._status.value}]\n"
                f"Total memory: {self._all_memory}\n"
                f"Used: {(self._use_memory / self._all_memory) * 100:.1f}%\n"
                f"Tasks:\n{task_col}")


class ProxyServer(Sersev):
    def __init__(self, name: str, max_tasks: int = 10, ping: int = 30,
                 target_server: Optional[Sersev] = None) -> None:
        super().__init__(name, max_tasks)
        self._ping: int = ping
        self._target_server: Optional[Sersev] = target_server
        if not isinstance(self._target_server, Sersev) and self._target_server is not None:
            raise TypeError("Target must be a Sersev instance")

    def take_target(self, target: Sersev) -> None:
        if not isinstance(target, Sersev):
            raise TypeError("Target must be a Sersev instance")
        self._target_server = target

    def pull_task(self, num: int) -> str:
        if self._target_server is None:
            raise ValueError("No target server set")
        if self._target_server.max_tasks <= len(self._target_server._tasks):
            raise BufferError(f"Server {self._target_server._name} is full.")
        task: str = self._tasks.pop(num)
        self._target_server.add_task(task)
        return f"Task redirected to {self._target_server._name}."

    def set_maintenance(self) -> None:
        self._target_server = None
        self._status = ServiceStatus.MAINTENANCE
        print(f"Server {self._name} set to maintenance.")

    def display(self) -> str:
        return f"ProxyServer({self._name}, ping={self._ping})"

    def score(self) -> float:
        return 100.0 - float(self._ping)

    def __str__(self) -> str:
        return (f"Proxy server {self._name} [{self._status.value}] "
                f"with {self._ping} ms delay")

    def info(self) -> str:
        task_col: str = "\n".join(self._tasks)
        target_name: str = self._target_server.name if self._target_server else "None"
        return (f"Name: {self._name}\n"
                f"Ping: {self._ping} ms\n"
                f"Target: {target_name}\n"
                f"Tasks:\n{task_col}")