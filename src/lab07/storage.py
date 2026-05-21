"""
Сохранение и загрузка коллекции сервисов в JSON-файл.

Зачем это нужно?
- Данные должны сохраняться между запусками программы.
- При старте приложение загружает сервисы из JSON-файла.
- При выходе — сохраняет обратно.
- JSON выбран потому что: читаемый формат, встроен в Python, легко отлаживать.

Как работает:
1. save() — превращает объекты Sersev в словари, записывает в JSON.
2. load() — читает JSON, создаёт из словарей объекты Sersev обратно.
"""

import json
import os
from typing import List, Dict, Any

# Импортируем существующие классы (не переписываем их!)
# Sersev — базовый класс сервера, ServiceStatus — перечисление статусов
from src.lab01.model import Sersev, ServiceStatus
# Дочерние классы серверов из lab03
from src.lab03.models import ComputeServer, StorageServer, ProxyServer


# Словарь для восстановления типа сервера при загрузке.
# Ключ — строка с именем класса, значение — сам класс.
# Зачем: в JSON хранится строка "ComputeServer", а нам нужно создать ComputeServer().
SERVER_TYPE_MAP: Dict[str, type] = {
    "ComputeServer": ComputeServer,
    "StorageServer": StorageServer,
    "ProxyServer": ProxyServer,
    "Sersev": Sersev,
}


def _service_to_dict(service: Sersev) -> Dict[str, Any]:
    """
    Превращает объект сервиса в словарь для JSON-сериализации.
    
    Как работает:
    - Берёт базовые поля (имя, статус, задачи).
    - Проверяет тип через isinstance() — для каждого типа сервера 
      добавляет специфичные поля (cpu_power для ComputeServer и т.д.).
    - Возвращает словарь, который json.dump может записать в файл.
    """
    data: Dict[str, Any] = {
        "type": type(service).__name__,  # "ComputeServer", "Sersev" и т.д.
        "name": service.name,
        "status": service.status,
        "max_tasks": service.max_tasks,
        "tasks": list(service._tasks),  # _tasks — приватное поле, но для сериализации нужен доступ
    }
    # Для каждого подкласса сохраняем его дополнительные атрибуты
    if isinstance(service, ComputeServer):
        data["cpu_power"] = service._cpu_power
    elif isinstance(service, StorageServer):
        data["all_memory"] = service._all_memory
    elif isinstance(service, ProxyServer):
        data["ping"] = service._ping
        data["target_name"] = service._target_server.name if service._target_server else None
    return data


def _dict_to_service(data: Dict[str, Any]) -> Sersev:
    """
    Восстанавливает объект сервиса из словаря (обратная операция к _service_to_dict).
    
    Как работает:
    - Берёт тип из словаря, создаёт экземпляр нужного класса.
    - Восстанавливает задачи, обходя ограничение max_tasks (добавляем через _tasks напрямую).
    - Восстанавливает статус (перебираем ServiceStatus).
    """
    # Получаем класс по строке типа, если тип неизвестен — используем Sersev
    srv_type: type = SERVER_TYPE_MAP.get(data["type"], Sersev)
    name: str = data["name"]
    max_tasks: int = data.get("max_tasks", 10)
    tasks: List[str] = data.get("tasks", [])

    # Создаём объект нужного типа с соответствующими параметрами
    if srv_type == ComputeServer:
        cpu_power: float = data.get("cpu_power", 0.5)
        service = ComputeServer(name, cpu_power, max_tasks)
    elif srv_type == StorageServer:
        all_memory: int = data.get("all_memory", 40)
        service = StorageServer(name, all_memory)
    elif srv_type == ProxyServer:
        ping: int = data.get("ping", 30)
        service = ProxyServer(name, max_tasks, ping)
    else:
        service = Sersev(name, max_tasks)

    # Добавляем задачи напрямую в _tasks, чтобы обойти проверки add_task()
    # (при загрузке мы доверяем сохранённым данным)
    for task in tasks:
        service._tasks.append(task)

    # Восстанавливаем статус из строки
    status_str: str = data.get("status", "idle")
    for st in ServiceStatus:
        if st.value == status_str:
            service._status = st
            break
    return service


def save(collection: List[Sersev], filepath: str) -> None:
    """
    Сохраняет коллекцию сервисов в JSON-файл.
    
    Args:
        collection: список объектов Sersev для сохранения
        filepath: путь к файлу (например, "data/services.json")
    
    Алгоритм:
    1. Создаём директорию, если её нет.
    2. Превращаем каждый сервис в словарь через _service_to_dict().
    3. Записываем список словарей в JSON.
    """
    dir_path: str = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    data: List[Dict[str, Any]] = [_service_to_dict(s) for s in collection]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  # indent=2 для читаемости


def load(filepath: str) -> List[Sersev]:
    """
    Загружает объекты сервисов из JSON-файла.
    
    Args:
        filepath: путь к файлу для загрузки
    
    Returns:
        список восстановленных объектов Sersev (пустой список, если файла нет)
    
    Алгоритм:
    1. Проверяет, существует ли файл.
    2. Читает JSON, получает список словарей.
    3. Каждый словарь превращает в объект через _dict_to_service().
    """
    if not os.path.exists(filepath):
        return []  # первый запуск — файла ещё нет

    with open(filepath, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)

    return [_dict_to_service(item) for item in data]