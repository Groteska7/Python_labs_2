#!/usr/bin/env python3
"""Демонстрация работы ЛР-5: функции как аргументы, стратегии и делегаты."""

from src.lab01.model import Sersev, ServiceStatus
from src.lab05.collection import SersevList
from src.lab05.strategies import (
    by_name,
    by_max_tasks,
    by_status_then_name,
    is_working,
    is_available,
    highlight,
    make_load_filter,
    StatusFilter,
    TaskReducer,
    DiscountStrategy
)
from src.lib_file import line_line


def run_demo():
    """Основная функция демонстрации."""
    LEN = 80

    print("\n" + line_line(row="ЛАБОРАТОРНАЯ РАБОТА №5: Стратегии и функциональное программирование", ln=LEN, dot="="))

    # Создаём тестовые сервисы
    s1 = Sersev("Alpha", max_tasks=5)
    s2 = Sersev("Beta", max_tasks=3)
    s3 = Sersev("Gamma", max_tasks=8)
    s4 = Sersev("Delta", max_tasks=4)
    s5 = Sersev("Epsilon", max_tasks=6)

    # Добавляем задачи (кроме одной, чтобы была разная загрузка)
    for s in [s1, s2, s3, s4, s5]:
        for i in range(s.max_tasks - 1):
            s.add_task(f"Задача_{i+1}")

    # Переводим Beta в режим обслуживания
    s2.set_maintenance()

    # Создаём основную коллекцию
    collection = SersevList("ОсновнаяКоллекция")
    for s in [s1, s2, s3, s4, s5]:
        collection.add_service(s)

    # ========== СЦЕНАРИЙ 1: полная цепочка операций ==========
    print("\n" + line_line(row="СЦЕНАРИЙ 1: Полная цепочка (фильтр -> сортировка -> преобразование)", ln=LEN, dot="-"))

    # Создаём отдельную коллекцию для цепочки, чтобы не портить исходную
    chain = SersevList("Цепочка")
    for s in [s1, s2, s3, s4, s5]:
        chain.add_service(s)

    result = (chain
              .filter_by(is_working)           # оставляем только работающие
              .sort_by(by_max_tasks)           # сортируем по макс. задачам
              .apply(highlight))               # переводим имена в ВЕРХНИЙ РЕГИСТР

    print("Результат после filter_by(is_working) -> sort_by(by_max_tasks) -> apply(highlight):")
    for i, s in enumerate(result):
        print(f"  {i+1}. {s}")

    # ========== СЦЕНАРИЙ 2: замена стратегий ==========
    print("\n" + line_line(row="СЦЕНАРИЙ 2: Замена стратегий сортировки", ln=LEN, dot="-"))

    fresh = SersevList("СвежаяКоллекция")
    for s in [s1, s2, s3, s4, s5]:
        fresh.add_service(s)

    print("Сортировка по имени (sorted(коллекция, key=by_name)):")
    sorted_by_name = sorted(fresh, key=by_name)
    for s in sorted_by_name:
        print(f"  - {s.name}")

    print("\nСортировка по максимальному количеству задач (sorted(коллекция, key=lambda x: x.max_tasks)):")
    sorted_by_tasks = sorted(fresh, key=lambda x: x.max_tasks)
    for s in sorted_by_tasks:
        print(f"  - {s.name} (макс. задач: {s.max_tasks})")

    print("\nСортировка по статусу, затем по имени:")
    sorted_by_status = sorted(fresh, key=by_status_then_name)
    for s in sorted_by_status:
        print(f"  - {s.name} (статус: {s.status})")

    # ========== СЦЕНАРИЙ 3: Callable-объекты (классы-стратегии) ==========
    print("\n" + line_line(row="СЦЕНАРИЙ 3: Callable-объекты (классы-стратегии)", ln=LEN, dot="-"))

    fresh2 = SersevList("СвежаяКоллекция2")
    for s in [s1, s2, s3, s4, s5]:
        fresh2.add_service(s)

    filter_working = StatusFilter(ServiceStatus.WORKING.value)
    print("Использование StatusFilter (callable-объект):")
    working_only = list(filter(filter_working, fresh2))
    for s in working_only:
        print(f"  - {s.name} (статус: {s.status})")

    reducer = TaskReducer(factor=0.5)
    print("\nДо применения TaskReducer:")
    for s in fresh2:
        print(f"  - {s.name}: {len(s._tasks)} задач")

    fresh2.apply(reducer)

    print("\nПосле применения TaskReducer (factor=0.5):")
    for s in fresh2:
        print(f"  - {s.name}: {len(s._tasks)} задач")

    # ========== ДЕМОНСТРАЦИЯ map() ==========
    print("\n" + line_line(row="ДЕМОНСТРАЦИЯ: преобразование через map()", ln=LEN, dot="-"))

    fresh3 = SersevList("СвежаяКоллекция3")
    for s in [s1, s2, s3, s4, s5]:
        fresh3.add_service(s)

    names = list(map(lambda x: x.name, fresh3))
    print("Извлечение имён через map(lambda x: x.name, коллекция):")
    print(f"  {names}")

    # ========== ДЕМОНСТРАЦИЯ фабрики функций ==========
    print("\n" + line_line(row="ДЕМОНСТРАЦИЯ: Фабрика функций", ln=LEN, dot="-"))

    fresh4 = SersevList("СвежаяКоллекция4")
    for s in [s1, s2, s3, s4, s5]:
        fresh4.add_service(s)

    load_filter = make_load_filter(30)
    high_load = list(filter(load_filter, fresh4))
    print("Сервисы с загрузкой >= 30% (через фабрику make_load_filter(30)):")
    for s in high_load:
        print(f"  - {s.name}: загрузка {s.load_percentage:.1f}%")

    # ========== СРАВНЕНИЕ lambda и именованной функции ==========
    print("\n" + line_line(row="ДЕМОНСТРАЦИЯ: lambda vs именованная функция", ln=LEN, dot="-"))

    fresh5 = SersevList("СвежаяКоллекция5")
    for s in [s1, s2, s3, s4, s5]:
        fresh5.add_service(s)

    print("Одинаковый результат через именованную функцию (by_name):")
    by_name_result = sorted(fresh5, key=by_name)
    for s in by_name_result:
        print(f"  - {s.name}")

    print("\nОдинаковый результат через lambda:")
    lambda_result = sorted(fresh5, key=lambda x: x.name)
    for s in lambda_result:
        print(f"  - {s.name}")

    # ========== ДЕМОНСТРАЦИЯ методов sort_by() / filter_by() ==========
    print("\n" + line_line(row="ДЕМОНСТРАЦИЯ: методы sort_by() и filter_by()", ln=LEN, dot="-"))

    fresh6 = SersevList("СвежаяКоллекция6")
    for s in [s1, s2, s3, s4, s5]:
        fresh6.add_service(s)

    fresh6.sort_by(by_max_tasks)
    print("После sort_by(by_max_tasks):")
    for s in fresh6:
        print(f"  - {s.name} (макс. задач: {s.max_tasks})")

    fresh6.filter_by(is_available)
    print("\nПосле filter_by(is_available) (исключены сервисы в состоянии ERROR):")
    for s in fresh6:
        print(f"  - {s.name} (статус: {s.status})")

    # ========== ДОПОЛНИТЕЛЬНО: демонстрация DiscountStrategy ==========
    print("\n" + line_line(row="ДОПОЛНИТЕЛЬНО: Стратегия скидки DiscountStrategy", ln=LEN, dot="-"))

    fresh7 = SersevList("СвежаяКоллекция7")
    for s in [s1, s2, s3, s4, s5]:
        fresh7.add_service(s)

    # Добавим демо-поле price к сервисам (если его нет в модели)
    # В данном случае просто показываем применение стратегии
    discount_strategy = DiscountStrategy(0.85)
    print("Применение DiscountStrategy (callable-объект):")
    print("  Стратегия применена ко всем сервисам коллекции")
    fresh7.apply(discount_strategy)
    print("  Готово!")

    # ========== ФИНАЛ ==========
    print("\n" + line_line(row="ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА", ln=LEN, dot="="))


if __name__ == "__main__":
    run_demo()