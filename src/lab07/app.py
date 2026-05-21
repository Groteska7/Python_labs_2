"""
Бизнес-логика приложения (средний слой).

Что здесь происходит:
- Этот файл — прослойка между cli.py (ввод/вывод) и моделями из lab01/lab03.
- CLI не знает о коллекции напрямую — все операции через App.
- App хранит коллекцию TypedCollection[Sersev] из lab06.
  Почему TypedCollection, а не SersevList из lab02/lab05?
  - TypedCollection из lab06 — generic-коллекция с методами find(), filter(), map().
  - find_by_name() возвращает Optional[T] (None, если не найден), а не строку ошибки как в lab02.
  - Это избавляет от костыля _find_by_name_raw в app.py.
  - Умная типизация через Generic[T] — коллекция знает тип элементов.
- При создании App загружает данные из JSON (storage.py).
- При выходе вызывается save_data() для сохранения.

Зачем нужен отдельный слой бизнес-логики?
- Чтобы CLI был "глупым" — только показывает меню и вызывает методы App.
- Если захотим сделать GUI или API — берём этот же App, не трогая CLI.
- Все проверки и исключения предметной области здесь.
"""

import os
from typing import List, Optional, Callable

# Импорты из предыдущих лабораторных — НЕ ПЕРЕПИСЫВАЕМ их
from src.lab01.model import Sersev, ServiceStatus  # базовый класс и статусы
from src.lab03.models import ComputeServer, StorageServer, ProxyServer  # дочерние классы
# TypedCollection из lab06 — generic-коллекция с type hints, find(), filter(), map()
# find_by_name() возвращает Optional[T] — нормальный None, а не строку ошибки как в lab02
from src.lab06.container import TypedCollection

# Наши собственные модули
from src.lab07.exceptions import ItemNotFoundError, DuplicateItemError
from src.lab07.storage import save, load


# Путь к файлу данных: data/services.json в той же папке, где лежит app.py
# __file__ — встроенная переменная, хранящая путь к текущему файлу
DATA_FILE: str = os.path.join(os.path.dirname(__file__), "data", "services.json")


class App:
    """
    Главный класс-менеджер.
    Содержит все операции над коллекцией сервисов.
    Внутри использует TypedCollection[Sersev] из lab06.
    """

    def __init__(self) -> None:
        """
        Конструктор:
        1. Создаёт пустую коллекцию TypedCollection[Sersev].
        2. Загружает в неё данные из JSON-файла (если файл существует).
        3. Если это первый запуск — коллекция пуста.
        """
        # TypedCollection[Sersev] — generic, T = Sersev,
        # поэтому add() принимает только Sersev и наследников
        self._collection: TypedCollection[Sersev] = TypedCollection[Sersev]("services")
        self._load_data()  # автозагрузка при старте

    def _load_data(self) -> None:
        """Загружает данные из JSON-файла и добавляет их в коллекцию."""
        services: List[Sersev] = load(DATA_FILE)
        for s in services:
            self._collection.add(s)  # TypedCollection.add() — добавляет элемент

    def save_data(self) -> None:
        """Сохраняет все сервисы в JSON-файл."""
        # self._collection.get_all() — возвращает копию списка
        save(self._collection.get_all(), DATA_FILE)

    def get_all(self) -> List[Sersev]:
        """
        Возвращает копию списка всех сервисов.
        Возвращаем копию (get_all()), чтобы внешний код не мог случайно изменить
        нашу внутреннюю коллекцию.
        """
        return self._collection.get_all()  # TypedCollection.get_all() -> List[T]

    def count(self) -> int:
        """Возвращает количество сервисов в коллекции."""
        return len(self._collection)

    def add_service(self, service: Sersev) -> None:
        """
        Добавляет сервис в коллекцию.
        
        Проверки:
        - Если сервис с таким именем уже есть — выбрасываем DuplicateItemError.
        - Если всё ок — добавляем через TypedCollection.add().
        
        Почему не используем TypedCollection.add_service?
        - У TypedCollection нет add_service — только add().
        - add() не проверяет дубликаты — это наша бизнес-логика.
        """
        # find_by_name() из lab06 возвращает None, а не строку ошибки
        # (в отличие от lab02, где возвращается строка "Элемент не найден")
        existing: Optional[Sersev] = self._collection.find_by_name(service.name)
        if existing is not None:
            raise DuplicateItemError(service.name)  # имя занято
        self._collection.add(service)  # TypedCollection.add() поддерживает chaining (return self)

    def remove_by_name(self, name: str) -> None:
        """
        Удаляет сервис по имени.

        Алгоритм:
        1. Ищем сервис. Если не нашли — ItemNotFoundError.
        2. Если нашли — удаляем через TypedCollection.remove_by_name().
        
        Зачем проверять существование перед удалением?
        - remove_by_name в TypedCollection просто фильтрует список молча.
        - Нам нужно сказать пользователю, был ли удалён элемент.
        """
        existing: Optional[Sersev] = self._collection.find_by_name(name)
        if existing is None:
            raise ItemNotFoundError(name)  # нечего удалять
        self._collection.remove_by_name(name)  # TypedCollection.remove_by_name()

    def find_by_name(self, name: str) -> Sersev:
        """
        Находит сервис по имени. Если не найден — исключение.
        
        Используется в:
        - Пункт меню 3 (найти сервис)
        - Пункт меню 8 (детальная информация)
        """
        service: Optional[Sersev] = self._collection.find_by_name(name)
        if service is None:
            raise ItemNotFoundError(name)
        return service

    def find_by_index(self, index: int) -> Sersev:
        """
        Находит сервис по индексу (позиции в списке).
        
        TypedCollection.find_by_index() возвращает Optional[Sersev].
        """
        service: Optional[Sersev] = self._collection.find_by_index(index)
        if service is None:
            raise ItemNotFoundError(f"с индексом {index}")
        return service

    def search_by_attr(self, attr_name: str, value: str) -> List[Sersev]:
        """
        Поиск сервисов по значению атрибута (частичное совпадение).
        
        Атрибуты для поиска:
        - name — по имени сервиса (регистронезависимо)
        - status — по статусу (idle/working/error/maintenance)
        - type — по типу сервера (Sersev/ComputeServer и т.д.)
        
        Частичное совпадение — строка "server" найдёт "MyServer" и "Server01".
        
        Используется: пункт меню 5.
        
        Зачем ручной перебор, а не TypedCollection.filter()?
        - filter() принимает предикат (bool), а у нас ещё и значение.
        - Можно было бы сделать filter() с lambda, но так нагляднее для обучения.
        """
        results: List[Sersev] = []
        for service in self._collection:  # перебираем все сервисы через __iter__
            if attr_name == "name" and value.lower() in service.name.lower():
                results.append(service)
            elif attr_name == "status" and value.lower() in service.status.lower():
                results.append(service)
            elif attr_name == "type" and value.lower() in type(service).__name__.lower():
                # type(service).__name__ — строка типа: "ComputeServer", "StorageServer"
                results.append(service)
        return results

    def filter_by_load(self, min_load: float, max_load: float) -> List[Sersev]:
        """
        Фильтрует сервисы по диапазону загрузки (0-100%).
        
        Использует TypedCollection.filter() с lambda-предикатом.
        filter() из lab06 принимает Callable[[T], bool] и возвращает List[T].
        
        load_percentage — свойство из Sersev, вычисляемое как len(tasks)/max_tasks*100.
        """
        return self._collection.filter(lambda s: min_load <= s.load_percentage <= max_load)

    def filter_by_status(self, status: str) -> List[Sersev]:
        """
        Фильтрует сервисы по статусу.
        
        Использует TypedCollection.filter() как в filter_by_load.
        
        s.status возвращает строку через @property из Sersev.
        """
        return self._collection.filter(lambda s: s.status == status)

    def sort_by_key(self, key_func: Callable[[Sersev], object], reverse: bool = False) -> List[Sersev]:
        """
        Сортирует копию коллекции по переданной функции-ключу (стратегии сортировки).
        
        Не изменяет оригинальную коллекцию — возвращает новый список.
        
        key_func — стратегия сортировки из lab05/strategies.py:
        - by_name — по имени
        - by_max_tasks — по макс. задачам  
        - by_load — по загрузке
        
        reverse=True — по убыванию, False — по возрастанию.
        
        Зачем sorted(), а не TypedCollection.map()?
        - map() преобразует элементы, а не сортирует.
        - Типизированная сортировка — отдельная операция.
        """
        return sorted(self._collection, key=key_func, reverse=reverse)

    def edit_service_tasks(self, name: str, new_tasks: List[str]) -> None:
        """
        Заменяет список задач сервиса.
        
        Алгоритм:
        1. Находим сервис по имени (find_by_name).
        2. Очищаем его задачи (прямой доступ к _tasks — да, это нарушение инкапсуляции,
           но для бизнес-логики это простительно).
        3. Добавляем новые задачи по одной через Sersev.add_task().
           Если сервис в состоянии ERROR — add_task() выбросит RuntimeError.
        """
        service: Sersev = self.find_by_name(name)
        service._tasks.clear()  # очищаем всё (обращаемся к protected-полю)
        for task in new_tasks:
            try:
                service.add_task(task)  # Sersev.add_task() — с проверками статуса
            except (RuntimeError, OverflowError):
                break  # сервис в ERROR или переполнен — стоп