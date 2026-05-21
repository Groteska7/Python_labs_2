"""
Интерфейс командной строки (верхний слой).

Зачем это нужно:
- Это "лицо" программы — пользователь видит меню и вводит команды.
- Здесь только ввод/вывод (input/print). Никакой бизнес-логики.
- Все операции делегируются App (слой бизнес-логики).
- Если захотим сделать графический интерфейс — перепишем только этот файл.

Как работает:
- Главная функция run(app) запускает бесконечный цикл.
- В каждом шаге: печатаем меню → ждём ввод → вызываем нужный обработчик.
- После каждого действия ждём Enter (чтобы пользователь успел прочитать результат).
- При выборе 0 (выход) — сохраняем данные и выходим из цикла.

Обработка ошибок:
- try/except ловит исключения ItemNotFoundError, DuplicateItemError,
  InvalidInputError и выводит понятные сообщения на русском.
"""

import os
from typing import List, Optional

# Импорты из lab01 и lab03 — существующие классы, не переписываем
from src.lab01.model import Sersev
from src.lab03.models import ComputeServer, StorageServer, ProxyServer

# Стратегии из lab05 — функции для сортировки по имени/задачам/загрузке
from src.lab05.strategies import by_name, by_max_tasks, by_load

# Наши модули
from src.lab07.app import App
from src.lab07.exceptions import ItemNotFoundError, DuplicateItemError, InvalidInputError

# Импортируем функцию для форматирования заголовков из общего lib_file
# line_line(row, ln, dot) — центрирует текст в рамке из символов dot
# Используется во всех предыдущих лабах для единообразного вывода
from src.lib_file import line_line


# ===================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ВЫВОДА =====================
def _clear_screen() -> None:
    """Очищает экран терминала (работает на Windows, Linux, macOS)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _print_header(title: str) -> None:
    """
    Выводит заголовок с помощью line_line из lib_file.
    Пример:
    ===================== ДОБАВЛЕНИЕ СЕРВИСА =====================
    """
    print()
    print(line_line(row=f" {title} ", ln=60, dot="="))


def _print_table(services: List[Sersev]) -> None:
    """
    Выводит список сервисов в виде отформатированной таблицы.
    
    Зачем таблица, а не просто print(s)?
    - Много сервисов — данные сливаются в нечитаемую кашу.
    - Таблица выравнивает колонки: #, Имя, Тип, Статус, Загрузка, Задачи.
    - Сразу видно общую картину.
    
    Форматирование:
    - {:<4} — выравнивание влево, ширина 4 символа (для номера).
    - {:<20} — имя, ширина 20.
    - и т.д.
    """
    if not services:
        print("  Коллекция пуста.")
        return

    # Заголовок таблицы
    header: str = f"{'#':<4} {'Имя':<20} {'Тип':<18} {'Статус':<13} {'Загрузка':<10} {'Задачи':<8}"
    print()
    print(header)
    print("-" * len(header))  # разделитель

    # Строки с данными
    for i, s in enumerate(services, 1):
        srv_type: str = type(s).__name__  # "ComputeServer", "Sersev" и т.д.
        load: str = f"{s.load_percentage:.1f}%"  # загрузка с одним знаком после запятой
        tasks: str = f"{len(s._tasks)}/{s.max_tasks}"  # "3/5" — текущие/максимум
        print(f"{i:<4} {s.name:<20} {srv_type:<18} {s.status:<13} {load:<10} {tasks:<8}")

    print("-" * len(header))
    print(f"  Всего: {len(services)}")


def _print_service_detail(service: Sersev) -> None:
    """
    Выводит детальную информацию о конкретном сервисе.
    Использует метод info() из модели Sersev (lab01) или переопределённый
    info() из дочерних классов (lab03).
    
    Для ComputeServer info() покажет CPU power.
    Для StorageServer — объём памяти.
    Для ProxyServer — пинг и целевой сервер.
    """
    print()
    print("─" * 40)
    print(service.info())  # полиморфный вызов — метод разный для разных классов
    print("─" * 40)


# ===================== ФУНКЦИИ ВВОДА С ВАЛИДАЦИЕЙ =====================

def _input_int(prompt: str) -> int:
    """
    Безопасный ввод целого числа.
    
    Зачем своя функция?
    - int(input()) выбрасывает ValueError, если введены буквы.
    - Мы перехватываем ValueError и выбрасываем своё InvalidInputError.
    - InvalidInputError ловится в главном цикле и выводит русское сообщение.
    """
    try:
        return int(input(prompt))
    except ValueError:
        raise InvalidInputError("Ошибка: введите число")


def _input_float(prompt: str) -> float:
    """
    Безопасный ввод числа с плавающей точкой.
    Аналогично _input_int(), но для float (для ввода мощности CPU, загрузки и т.д.).
    """
    try:
        return float(input(prompt))
    except ValueError:
        raise InvalidInputError("Ошибка: введите число")


def _confirm(prompt: str) -> bool:
    """
    Запрашивает подтверждение у пользователя.
    
    Используется для опасных операций (удаление).
    Возвращает True, если пользователь ввёл "y", "yes", "д", "да".
    Иначе — False.
    
    Зачем? Чтобы случайно не удалить важные данные.
    """
    answer: str = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ("y", "yes", "д", "да")


def _choose_server_type() -> str:
    """
    Выбор типа сервера через подменю.
    
    Возвращает строку:
    - "Sersev" — обычный сервер
    - "ComputeServer" — вычислительный
    - "StorageServer" — сервер хранения
    - "ProxyServer" — прокси
    
    Зачем выбор типа?
    - Мы используем иерархию классов из lab01/lab03.
    - Пользователь может создать любой тип сервера.
    - Каждый тип имеет свои поля (cpu_power, all_memory, ping).
    """
    print("  Выберите тип сервера:")
    print("    1. Обычный сервер (Sersev)")
    print("    2. Вычислительный сервер (ComputeServer)")
    print("    3. Сервер хранения (StorageServer)")
    print("    4. Прокси-сервер (ProxyServer)")
    choice: int = _input_int("  Ваш выбор: ")
    types: List[str] = ["Sersev", "ComputeServer", "StorageServer", "ProxyServer"]
    if 1 <= choice <= 4:
        return types[choice - 1]
    raise InvalidInputError("Неверный выбор типа сервера")


def _create_service(name: str, srv_type: str, app: App) -> Sersev:
    """
    Создаёт объект сервера указанного типа.
    
    Алгоритм:
    - В зависимости от типа запрашиваем дополнительные параметры.
    - Создаём экземпляр соответствующего класса.
    - Возвращаем его.
    
    Пример:
    srv_type = "ComputeServer", name = "Comp1"
    → запрашиваем cpu_power
    → создаём ComputeServer("Comp1", 2.5)
    """
    if srv_type == "ComputeServer":
        cpu: float = _input_float("  Введите мощность CPU: ")
        mt: int = _input_int("  Введите максимальное кол-во задач: ")
        return ComputeServer(name, cpu, mt)
    elif srv_type == "StorageServer":
        memory: int = _input_int("  Введите объём памяти: ")
        return StorageServer(name, memory)
    elif srv_type == "ProxyServer":
        ping: int = _input_int("  Введите пинг (ms): ")
        mt: int = _input_int("  Введите максимальное кол-во задач: ")
        flag: bool = _confirm("  хотите указать целевой сервер?\n")
        if flag:
            _handle_list(app)
            target: str = input("    Введите имя целевого сервера: ")
            target: Sersev = app.find_by_name(target)
            return ProxyServer(name, mt, ping, target_server=target)
        else:
            return ProxyServer(name, mt, ping)
    else:  # Sersev
        max_tasks: int = _input_int("  Введите макс. задач: ")
        return Sersev(name, max_tasks)


# ===================== ГЛАВНЫЙ ЦИКЛ МЕНЮ =====================

def run(app: App) -> None:
    """
    Запускает главный цикл CLI-меню.
    
    Это сердце приложения:
    1. Печатаем меню.
    2. Ждём ввод пользователя.
    3. Вызываем соответствующий обработчик.
    4. Ждём Enter, чтобы пользователь прочитал результат.
    5. Повторяем, пока не выбран пункт 0.
    
    Обработка ошибок:
    - Все исключения ловятся здесь.
    - Пользователь видит русское описание проблемы.
    - После ошибки цикл продолжается (программа не падает).
    """
    while True:
        # Очищаем консоль перед каждым показом меню,
        # чтобы не засорять экран старыми выводами
        os.system("cls" if os.name == "nt" else "clear")
        _print_header("МЕНЮ УПРАВЛЕНИЯ СЕРВИСАМИ")
        print("  1. Добавить сервис")
        print("  2. Показать все сервисы")
        print("  3. Найти сервис")
        print("  4. Удалить сервис")
        print("  5. Поиск по атрибуту")
        print("  6. Фильтрация")
        print("  7. Сортировка")
        print("  8. Детальная информация о сервисе")
        print("  9. редактирование информации о сервисе")
        print("  0. Выход")
        print("-" * 60)

        # Ввод пункта меню. Если ввели не число — InvalidInputError, продолжаем.
        try:
            choice: int = _input_int("  Выберите пункт: ")
        except InvalidInputError as e:
            print(f"  {e}")
            continue

        print()

        # Обработка выбора
        try:
            if choice == 0:
                # Выход: сохраняем данные и завершаем цикл
                app.save_data()
                print("  бай")
                break

            elif choice == 1:
                _handle_add(app)

            elif choice == 2:
                _handle_list(app)

            elif choice == 3:
                _handle_find(app)

            elif choice == 4:
                _handle_remove(app)

            elif choice == 5:
                _handle_search(app)

            elif choice == 6:
                _handle_filter(app)

            elif choice == 7:
                _handle_sort(app)

            elif choice == 8:
                _handle_detail(app)
            elif choice == 9:
                _handle_edit(app)

            else:
                print("  Неверный пункт меню. Выберите от 0 до 8.")

        # Ловим наши исключения и выводим понятные сообщения
        except ItemNotFoundError as e:
            print(f"  Ошибка: {e}")
        except DuplicateItemError as e:
            print(f"  Ошибка: {e}")
        except InvalidInputError as e:
            print(f"  {e}")
        except Exception as e:
            # Любая другая ошибка — на всякий случай
            print(f"  Непредвиденная ошибка: {e}")

        _wait_enter()


def _wait_enter() -> None:
    """
    Пауза: ждём, пока пользователь нажмёт Enter.
    
    Зачем?
    - После вывода результатов меню снова печатается.
    - Без паузы пользователь не успеет прочитать результат.
    - Пауза даёт время изучить таблицу/информацию.
    """
    input("  Нажмите Enter для продолжения...")


# ===================== ОБРАБОТЧИКИ ПУНКТОВ МЕНЮ =====================

def _handle_edit(app: App) -> None:
    _clear_screen()
    _print_header("редактирование информации о сервисе")
    name: str = input("  Введите имя сервиса: ").strip()
    if not name:
        raise InvalidInputError("Имя не может быть пустым")
    if app._collection.find_by_name(name) is None:
        raise ItemNotFoundError(name)
    tasks_raw: list[str] = input("  Введите новый список задач через запятую: ").split(",")
    tasks = [task.strip() for task in tasks_raw if task.strip()]
    app.edit_service_tasks(name, tasks)

def _handle_add(app: App) -> None:
    """
    Обработчик "Добавить сервис" (пункт 1).
    
    Сценарий:
    1. Вводим имя.
    2. Выбираем тип сервера (1-4).
    3. Вводим доп. параметры (CPU, память, пинг или макс. задач).
    4. Вызываем app.add_service().
    
    Если сервис с таким именем уже есть — App выбросит DuplicateItemError,
    который ловится в главном цикле.
    """
    _clear_screen()
    _print_header("ДОБАВЛЕНИЕ СЕРВИСА")
    name: str = input("  Введите имя сервиса: ").strip()
    if not name:
        raise InvalidInputError("Имя не может быть пустым")

    srv_type: str = _choose_server_type() # ранее можно видеть функцию _choose_server_type, которая вызывает минюшку., и выпрашивает у пользователя тип сервера. тут она его и возвращает.
    service: Sersev = _create_service(name, srv_type, app)
    app.add_service(service)
    print(f"  Сервис '{name}' успешно добавлен!")


def _handle_list(app: App) -> None:
    """
    Обработчик "Показать все сервисы" (пункт 2).
    
    Просто получает все сервисы из App и выводит таблицу.
    Если коллекция пуста — _print_table выведет "Коллекция пуста."
    """
    _clear_screen()
    _print_header("ВСЕ СЕРВИСЫ")
    services: List[Sersev] = app.get_all()
    _print_table(services)


def _handle_find(app: App) -> None:
    """
    Обработчик "Найти сервис" (пункт 3).
    
    Ищет сервис по точному имени.
    Если найден — выводит детальную информацию.
    Если не найден — ItemNotFoundError.
    """
    _clear_screen()
    _print_header("ПОИСК СЕРВИСА")
    name: str = input("  Введите имя сервиса: ").strip()
    service: Sersev = app.find_by_name(name)
    _print_service_detail(service)


def _handle_remove(app: App) -> None:
    """
    Обработчик "Удалить сервис" (пункт 4).
    
    Сценарий:
    1. Вводим имя.
    2. Показываем детальную информацию (чтобы пользователь знал, что удаляет).
    3. Запрашиваем подтверждение (y/n).
    4. Если подтвердил — удаляем. Если нет — отменяем.
    
    Зачем подтверждение?
    - Удаление — опасная операция.
    - Пользователь мог ошибиться или передумать.
    """
    _clear_screen()
    _print_header("УДАЛЕНИЕ СЕРВИСА")
    name: str = input("  Введите имя сервиса для удаления: ").strip()
    service: Sersev = app.find_by_name(name)  # может выбросить ItemNotFoundError
    _print_service_detail(service)  # показываем, что удаляем
    if _confirm(f"  Удалить сервис '{name}'?"):
        app.remove_by_name(name)
        print(f"  Сервис '{name}' удалён.")
    else:
        print("  Удаление отменено.")


def _handle_search(app: App) -> None:
    """
    Обработчик "Поиск по атрибуту" (пункт 5).
    
    Позволяет искать сервисы по:
    - name — частичное совпадение имени (найдёт "Test" в "TestServer")
    - status — частичное совпадение статуса
    - type — частичное совпадение типа класса
    
    Возвращает таблицу со всеми подходящими сервисами.
    """
    _clear_screen()
    _print_header("ПОИСК ПО АТРИБУТУ")
    print("  Доступные атрибуты: name, status, type")
    attr: str = input("  Введите атрибут: ").strip().lower()
    if attr not in ("name", "status", "type"):
        raise InvalidInputError("Неверный атрибут. Доступны: name, status, type")
    value: str = input("  Введите значение для поиска: ").strip()
    results: List[Sersev] = app.search_by_attr(attr, value)
    _print_header(f"РЕЗУЛЬТАТЫ ПОИСКА ПО {attr} = '{value}'")
    _print_table(results)


def _handle_filter(app: App) -> None:
    """
    Обработчик "Фильтрация" (пункт 6).
    
    Два типа фильтрации:
    1. По диапазону загрузки (0-100%) — например, сервисы с загрузкой 30-80%.
    2. По статусу — рабочие, в ожидании, ошибочные, на обслуживании.
    
    Результат — отфильтрованная таблица.
    """
    _clear_screen()
    _print_header("ФИЛЬТРАЦИЯ СЕРВИСОВ")
    print("  1. По диапазону загрузки")
    print("  2. По статусу")
    filter_choice: int = _input_int("  Выберите тип фильтра: ")

    results: List[Sersev] = []
    if filter_choice == 1:
        # Фильтр по загрузке
        print()
        min_load: float = _input_float("  Минимальная загрузка (0-100): ")
        max_load: float = _input_float("  Максимальная загрузка (0-100): ")
        if min_load < 0 or max_load > 100 or min_load > max_load:
            raise InvalidInputError("Некорректный диапазон загрузки (0-100)")
        results = app.filter_by_load(min_load, max_load)
        _print_header(f"СЕРВИСЫ С ЗАГРУЗКОЙ {min_load}%-{max_load}%")
    elif filter_choice == 2:
        # Фильтр по статусу
        status: str = input("  Введите статус (idle, working, error, maintenance): ").strip().lower()
        valid_statuses: List[str] = ["idle", "working", "error", "maintenance"]
        if status not in valid_statuses:
            raise InvalidInputError(f"Неверный статус. Доступны: {', '.join(valid_statuses)}")
        results = app.filter_by_status(status)
        _print_header(f"СЕРВИСЫ СО СТАТУСОМ '{status}'")
    else:
        raise InvalidInputError("Неверный выбор фильтра")

    _print_table(results)


def _handle_sort(app: App) -> None:
    """
    Обработчик "Сортировка" (пункт 7).
    
    Стратегии сортировки (из lab05/strategies.py):
    1. По имени — by_name (алфавитный порядок)
    2. По макс. задачам — by_max_tasks
    3. По загрузке — by_load
    
    Можно выбрать порядок: по возрастанию (a) или по убыванию (d).
    
    Результат — отсортированная таблица.
    """
    _clear_screen()
    _print_header("СОРТИРОВКА СЕРВИСОВ")
    print("  1. По имени")
    print("  2. По макс. задачам")
    print("  3. По загрузке")
    sort_choice: int = _input_int("  Выберите стратегию сортировки: ")

    # Сопоставляем номер с функцией-стратегией из lab05
    key_map = {1: by_name, 2: by_max_tasks, 3: by_load}
    key_func = key_map.get(sort_choice)
    if key_func is None:
        raise InvalidInputError("Неверный выбор сортировки")

    # Порядок сортировки
    reverse: bool = False
    order: str = input("  По возрастанию (a) или по убыванию (d)? ").strip().lower()
    if order in ("d", "у", "desc", "убыв"):
        reverse = True
    elif order not in ("a", "ф", "asc", "возр"):
        print("  Используется порядок по возрастанию.")

    results: List[Sersev] = app.sort_by_key(key_func, reverse)
    _print_header(f"ОТСОРТИРОВАННЫЕ СЕРВИСЫ{' (по убыванию)' if reverse else ' (по возрастанию)'}")
    _print_table(results)


def _handle_detail(app: App) -> None:
    """
    Обработчик "Детальная информация" (пункт 8).
    
    Находит сервис по имени и выводит его детальный отчёт (метод info()).
    Для каждого типа сервера info() выдаёт разные данные:
    - Sersev: имя + задачи
    - ComputeServer: имя + CPU power + прогнозируемое время
    - StorageServer: имя + память + процент использования
    - ProxyServer: имя + пинг + целевой сервер + задачи
    """
    _clear_screen()
    _print_header("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ")
    name: str = input("  Введите имя сервиса: ").strip()
    service: Sersev = app.find_by_name(name)  # может выбросить ItemNotFoundError
    _print_service_detail(service)