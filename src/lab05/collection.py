from src.lab02.collection import SersevList as BaseSersevList

class SersevList(BaseSersevList):
    def __init__(self, name: str):
        super().__init__(name)

    def add_service(self, service):
        """Добавляет сервис и возвращает self для цепочек."""
        super().add_service(service)
        return self

    def sort_by(self, key_func):
        """Сортирует коллекцию по переданной функции-ключу."""
        self._services = sorted(self._services, key=key_func)
        return self

    def filter_by(self, predicate):
        """Фильтрует коллекцию по переданному предикату."""
        self._services = list(filter(predicate, self._services))
        return self

    def apply(self, func):
        """Применяет функцию ко всем элементам коллекции."""
        self._services = list(map(func, self._services))
        return self
