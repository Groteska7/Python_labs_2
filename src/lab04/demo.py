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