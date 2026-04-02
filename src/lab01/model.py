from enum import Enum

class ServiceStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class Sersev:
    VERSION = "1.0.5"

    def __init__(self, name: str, max_tasks: int = 10):
        # Закрытые атрибуты экземпляра
        self._name = self._validate_name(name)
        self._max_tasks = self._validate_max_tasks(max_tasks)
        self._tasks = []
        self._status = ServiceStatus.IDLE

    # --- Методы валидации (не дублируют код) ---
    def _validate_name(self, name: str) -> str:
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Имя сервиса должно быть непустой строкой")
        return name.strip()

    def _validate_max_tasks(self, limit: int) -> int:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Лимит задач должен быть целым числом больше 0")
        return limit

    # --- Свойства (Properties) ---
    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status.value

    @property
    def load_percentage(self):
        """Пример вычисляемого свойства"""
        return (len(self._tasks) / self._max_tasks) * 100

    @property
    def max_tasks(self):
        return self._max_tasks

    @max_tasks.setter
    def max_tasks(self, value: int):
        # Валидация при изменении через сеттер
        new_limit = self._validate_max_tasks(value)
        if new_limit < len(self._tasks):
            raise ValueError("Новый лимит меньше текущего количества задач!")
        self._max_tasks = new_limit

    # --- Бизнес-методы и состояние ---
    def add_task(self, task_name: str):
        """Добавление задачи с проверкой состояния"""
        if self._status == ServiceStatus.ERROR:
            raise RuntimeError("Нельзя добавить задачу: сервис в состоянии ERROR")
        
        if len(self._tasks) >= self._max_tasks:
            self._status = ServiceStatus.ERROR # Меняем состояние при перегрузке
            raise OverflowError(f"Сервис '{self._name}' переполнен!")
            
        self._tasks.append(task_name)
        self._status = ServiceStatus.WORKING

    def clear_tasks(self):
        """Очистка и перевод в режим ожидания"""
        self._tasks.clear()
        self._status = ServiceStatus.IDLE

    def set_maintenance(self):
        """Метод изменения состояния"""
        self._status = ServiceStatus.MAINTENANCE
        print(f"Сервис {self._name} переведен на тех. обслуживание.")

    def __str__(self):
        return f"Сервис '{self._name}' [{self._status.value}]. Загрузка: {len(self._tasks)}/{self._max_tasks}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Sersev):
            return False
        # Считаем сервисы равными, если у них одинаковые имена и лимиты
        return self._name == other._name and self._max_tasks == other._max_tasks