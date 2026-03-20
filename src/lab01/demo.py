from .model import Sersev
from ..lib_file import line_line

def run_demo():
    print()
    print(line_line(row="Тестирование Sersev v{Sersev.VERSION}", ln=60, dot="-"))

    # 1. Успешное создание
    s1 = Sersev("MainServer", max_tasks=4)
    s2 = Sersev("MainServer", max_tasks=4)
    print(f"Объект создан: {s1}")
    print(f"Сравнение (s1 == s2): {s1 == s2}")

    # 2. Демонстрация валидации при создании
    print()
    print(line_line(row="Проверка валидации", ln=60, dot="-"))
    try:
        invalid_s = Sersev("", -5)
    except ValueError as e:
        print(f"Поймана ошибка: {e}")
    
    # 3. Работа с бизнес-логикой и состояниями
    print()
    print(line_line(row="Сценарий: Заполнение задачами", ln=60))
    try:
        s1.add_task("Data Indexing")
        s1.add_task("Backup")
        s1.add_task("Log Rotation")
        s1.add_task("Updating logs")
        print(s1)
        print(f"Текущая нагрузка: {s1.load_percentage}%")
        
        print("Попытка превысить лимит...")
        s1.add_task("overcharge")
    except Exception as e:
        print(f"Результат: {e}")
        print(f"Статус после ошибки: {s1.status}")

    s1.clear_tasks()
    print()
    print(line_line(row="Сценарий: работа -> перевод в режим ожидания", ln=60))
    s1.add_task("Backup")
    s1.add_task("Updating logs")
    s1.add_task("Uploaading_data")
    print(s1)
    print(f"текущая нагрузка: {s1.load_percentage}%")
    print("перевод в режим ожидания")
    s1.clear_tasks()
    print(f"Статус сервера: {s1.status}")
    print()
    print(line_line("Сценарий: перевод в режим обслуживания",60))
    s1.add_task("Backup")
    s1.add_task("Updating logs")
    print(s1)
    print(f"текущая нагрузка: {s1.load_percentage}%")
    print(f"Статус сервера: {s1.status}")
    s1.set_maintenance()
    print(f"Статус сервера: {s1.status}")

    # 4. Работа сеттера
    print()
    print(line_line(row="Изменение лимита через setter", ln=60, dot="-"))
    s1.clear_tasks()
    s1.max_tasks = 100
    print(f"Новый лимит s1: {s1.max_tasks}")

    # 5. Атрибут класса
    print(f"\nВерсия через класс: {Sersev.VERSION}")
    print(f"Версия через экземпляр: {s1.VERSION}")
    print(f"Красивый вывод через f-str: {s1.__str__()}")

if __name__ == "__main__":
    run_demo()
