"""Стратегии для работы с коллекцией SersevList.

Содержит функции-предикаты, функции-ключи, фабрики функций
и callable-классы-стратегии для ЛР-5.
"""

from src.lab01.model import Sersev, ServiceStatus


# ============ Стратегии сортировки (ключи) ============

def by_name(item: Sersev) -> str:
    """Ключ сортировки по имени сервиса."""
    return item.name


def by_max_tasks(item: Sersev) -> int:
    """Ключ сортировки по максимальному количеству задач."""
    return item.max_tasks


def by_status_then_name(item: Sersev) -> tuple:
    """Ключ сортировки: сначала по статусу, затем по имени."""
    return (item.status, item.name)


def by_load(item: Sersev) -> float:
    """Ключ сортировки по проценту загрузки."""
    return item.load_percentage


# ============ Функции фильтрации (предикаты) ============

def is_working(item: Sersev) -> bool:
    """Фильтр: сервис в состоянии WORKING."""
    return item.status == ServiceStatus.WORKING.value


def is_available(item: Sersev) -> bool:
    """Фильтр: сервис НЕ в состоянии ERROR."""
    return item.status != ServiceStatus.ERROR.value


def is_idle(item: Sersev) -> bool:
    """Фильтр: сервис в состоянии IDLE."""
    return item.status == ServiceStatus.IDLE.value


# ============ Фабрика функций ============

def make_load_filter(min_load: float):
    """Фабрика: создаёт фильтр для сервисов с загрузкой >= min_load.
    
    Args:
        min_load: минимальный процент загрузки (0-100)
    
    Returns:
        функция-предикат, принимающая Sersev и возвращающая bool
    """
    def filter_fn(item: Sersev) -> bool:
        return item.load_percentage >= min_load
    return filter_fn


# ============ Функции преобразования ============

def highlight(item: Sersev) -> Sersev:
    """Преобразование: переводит имя сервиса в ВЕРХНИЙ РЕГИСТР."""
    item._name = item.name.upper()  # используем property для чтения
    return item


# ============ Callable-классы-стратегии ============

class StatusFilter:
    """Стратегия фильтрации по статусу (callable-объект)."""
    
    def __init__(self, status: str):
        self.status = status

    def __call__(self, item: Sersev) -> bool:
        return item.status == self.status


class TaskReducer:
    """Стратегия сокращения списка задач (callable-объект)."""
    
    def __init__(self, factor: float = 0.8):
        self.factor = factor

    def __call__(self, item: Sersev) -> Sersev:
        """Оставляет только часть задач (первые factor * длина)."""
        new_len = int(len(item._tasks) * self.factor)
        item._tasks = item._tasks[:new_len]
        return item


class DiscountStrategy:
    """Стратегия применения скидки (callable-объект)."""
    
    def __init__(self, factor: float = 0.9):
        self.factor = factor

    def __call__(self, item: Sersev) -> Sersev:
        # Так как в модели Sersev нет поля price,
        # стратегия может использоваться для других целей
        # Например, уменьшаем max_tasks как "скидку на мощность"
        if hasattr(item, 'price'):
            item.price = item.price * self.factor
        return item