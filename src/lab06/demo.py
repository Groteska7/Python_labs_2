"""Демонстрация работы ЛР-6: Generics, типизация и протоколы."""

from src.lab01.model import Sersev, ServiceStatus
from src.lab03.models import ComputeServer, StorageServer, ProxyServer
from src.lab06.container import TypedCollection, D, S
from src.lib_file import line_line


def run_demo() -> None:
    """Основная функция демонстрации."""
    LEN: int = 80

    # ========== 1. TypedCollection — базовое использование ==========
    print("\n" + line_line(row="1. TypedCollection — базовое использование", ln=LEN, dot="-"))

    # Создание коллекции
    tc: TypedCollection[Sersev] = TypedCollection[Sersev]("Серверы")

    # Создание тестовых сервисов
    s1 = Sersev("Alpha", max_tasks=5)
    s2 = Sersev("Beta", max_tasks=3)
    s3 = Sersev("Gamma", max_tasks=8)

    # Добавление задач для создания разной загрузки
    for i in range(s1.max_tasks - 1):
        s1.add_task(f"Задача_{i+1}")
    for i in range(s2.max_tasks - 1):
        s2.add_task(f"Задача_{i+1}")
    for i in range(s3.max_tasks - 1):
        s3.add_task(f"Задача_{i+1}")

    # Добавление в коллекцию
    tc.add(s1).add(s2).add(s3)

    # Вывод информации
    print(f"Коллекция: {tc}")
    print(f"Длина: {len(tc)}")
    print("Все элементы:")
    for item in tc:
        print(f"  - {item}")

    # ========== 2. find(), filter(), map() ==========
    print("\n" + line_line(row="2. find(), filter(), map()", ln=LEN, dot="-"))

    # find — поиск существующего
    найденный = tc.find(lambda x: x.name == "Alpha")
    print(f"find(имя=='Alpha'): {найденный}")

    # find — поиск отсутствующего
    не_найден = tc.find(lambda x: x.name == "НеСуществует")
    print(f"find(имя=='НеСуществует'): {не_найден}")

    # filter — фильтрация
    работающие = tc.filter(lambda x: x.status == ServiceStatus.WORKING.value)
    print(f"filter(работающие): найдено {len(работающие)} элементов")

    # map — преобразование в имена (T → str)
    имена: list[str] = tc.map(lambda x: x.name)
    print(f"map в имена: {имена}")

    # map — преобразование в загрузку (T → float)
    загрузки: list[float] = tc.map(lambda x: x.load_percentage)
    print(f"map в загрузку: {загрузки}")

    # ========== 3. TypedCollection[D] — протокол Displayable ==========
    print("\n" + line_line(row="3. TypedCollection[D] — протокол Displayable", ln=LEN, dot="-"))

    # Создание объектов разных типов
    вычисл_сервер = ComputeServer("C-01", cpu_power=2.0)
    хранилище = StorageServer("S-01", all_memory=100)
    прокси = ProxyServer("P-01", ping=15, target_server=вычисл_сервер)

    # Коллекция с ограничением Displayable
    коллекция_display: TypedCollection[D] = TypedCollection[D]("Отображаемые")
    коллекция_display.add(вычисл_сервер).add(хранилище).add(прокси)

    # Вызов display() для каждого
    print("TypedCollection[D] — вызов display():")
    for элемент in коллекция_display:
        print(f"  {элемент.display()}")

    # ========== 4. TypedCollection[S] — протокол Scorable ==========
    print("\n" + line_line(row="4. TypedCollection[S] — протокол Scorable", ln=LEN, dot="-"))

    # Коллекция с ограничением Scorable
    коллекция_score: TypedCollection[S] = TypedCollection[S]("Оцениваемые")
    коллекция_score.add(вычисл_сервер).add(хранилище).add(прокси)

    # Вызов score() для каждого
    print("TypedCollection[S] — вызов score():")
    for элемент in коллекция_score:
        print(f"  оценка = {элемент.score():.1f}")

    # map с преобразованием
    все_оценки: list[float] = коллекция_score.map(lambda x: x.score())
    print(f"Все оценки через map(): {все_оценки}")


if __name__ == "__main__":
    run_demo()