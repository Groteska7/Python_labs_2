"""
from ..lab01.model import Sersev, ServiceStatus, Manageable, Diagnosable
from ..lab03.models import ProxyServer, StorageServer, ComputeServer
from ..lab02.collection import SersevList

if __name__ == "__main__":

    com_s1=ComputeServer("C-01", cpu_power=1.5)
    stor_s1=StorageServer("S-99", all_memory=1024)
     
    bbs=SersevList("big_boss_storage")

    com_s1.add_task("Thinking_Troyan")
    com_s1.add_task("Bulling")
    com_s1.add_task("DDOS")

    stor_s1.add_task("Saving_Troyan")
    stor_s1.add_task("Loading_Savrs")
    stor_s1.add_task("Make_Backup")

    bbs.add_service(stor_s1)
    bbs.add_service(com_s1)



    for server in bbs:
        # Мы можем вызвать методы интерфейсов у любого объекта в списке
        server.set_maintenance() 
        if isinstance(server, Diagnosable):
            print(server.get_detailed_report())
        print("-" * 20)
        # --- ТЕСТ 1: Работа через универсальную функцию ---
    # Мы передаем список серверов в функцию, которая работает с ними как с Diagnosable
    process_server_diagnostics(list(bbs))

    # --- ТЕСТ 2: Массовое управление через интерфейс Manageable ---
    print("=== Тест массового техобслуживания ===")
    for server in bbs:
        # Проверка, поддерживает ли сервер управление (Manageable)
        if isinstance(server, Manageable):
            server.set_maintenance()
            print(f"Статус {server.name}: {server.status}")
        print("-" * 20)

    # --- ТЕСТ 3: Проверка специфики (ICloudSync) ---
    print("=== Тест специфических возможностей ===")
    # Только StorageServer должен отозваться на этот интерфейс
    if isinstance(stor_s1, ICloudSync):
        print(f"Сервер {stor_s1.name} поддерживает облако. Пробуем синхронизацию:")
        stor_s1.sync()
"""

from ..lab01.model import Sersev, ServiceStatus, Manageable, Diagnosable, ICloudSync
from ..lab03.models import ProxyServer, StorageServer, ComputeServer
from ..lab02.collection import SersevList

# Универсальная функция для Скриншота №3
def process_diagnostics(items: list[Diagnosable]):
    for item in items:
        if isinstance(item, Diagnosable):
            print(f"Обработка через интерфейс: {item.get_detailed_report()}")

if __name__ == "__main__":
    # Подготовка данных
    com_s1 = ComputeServer("C-01", cpu_power=1.5)
    stor_s1 = StorageServer("S-99", all_memory=1024)
    proxy_s1 = ProxyServer("P-Gateway", target_server=com_s1)
    
    com_s1.add_task("System_Calculation")
    stor_s1.add_task("Database_Backup")

    # --- СКРИНШОТ №1: Работа метода интерфейса Manageable ---
    print("\n" + "="*20)
    print("ТЕСТ: Интерфейс Manageable")
    print("="*20)
    com_s1.set_maintenance()
    stor_s1.set_maintenance()
    print(f"Статус {com_s1.name}: {com_s1.status}")
    print(f"Статус {stor_s1.name}: {stor_s1.status}")

    # --- СКРИНШОТ №2: Работа метода интерфейса Diagnosable (Разная реализация) ---
    print("\n" + "="*20)
    print("ТЕСТ: Интерфейс Diagnosable")
    print("="*20)
    print(com_s1.get_detailed_report())
    print(stor_s1.get_detailed_report())

    # --- СКРИНШОТ №3: Универсальная функция и интерфейс как тип ---
    print("\n" + "="*20)
    print("ТЕСТ: Универсальная функция")
    print("="*20)
    server_list = [com_s1, stor_s1]
    process_diagnostics(server_list)

    # --- СКРИНШОТ №4: Проверка через isinstance и множественная реализация ---
    print("\n" + "="*20)
    print("ТЕСТ: Проверка isinstance")
    print("="*20)
    for srv in [com_s1, stor_s1, proxy_s1]:
        print(f"Проверка {srv.name}:")
        if isinstance(srv, ICloudSync):
            print(f" [OK] Найдена поддержка ICloudSync")
            srv.sync()
        else:
            print(f" [X] Интерфейс ICloudSync не поддерживается")
