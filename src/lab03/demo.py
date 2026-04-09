from ..lab01.model import Sersev
from .models import StorageServer, ProxyServer, ComputeServer
from ..lab02.collection import SersevList
from ..lib_file import line_line

def run_demo():
    serv_1=Sersev("NoobSer")
    com_s1=ComputeServer("ComputeSerOne")
    stor_s1=StorageServer("StorageSerOne")
    prox_s1=ProxyServer("ProxySerOne")

    print(serv_1)
    print()
    print(com_s1)
    print()
    print(stor_s1)
    print()
    print(prox_s1)
    print()
    print()

    serv_1.add_task("Seeing_Troyan")
    serv_1.add_task("Stuping")

    com_s1.add_task("Thinking_Troyan")
    com_s1.add_task("Bulling")
    com_s1.add_task("DDOS"
                    )
    stor_s1.add_task("Saving_Troyan")
    stor_s1.add_task("Loading_Savrs")
    stor_s1.add_task("Make_Backup")
    # print(stor_s1.get_use_memory)

    prox_s1.add_task("send_YouToob")
    prox_s1.add_task("Uploading_data_D%.;or>")
    prox_s1.add_task("Spreading_Troyan")
    prox_s1.take_target(serv_1)

    bbs=SersevList("big_boss_storage")
    bbs.add_service(serv_1)
    bbs.add_service(com_s1)
    bbs.add_service(stor_s1)
    bbs.add_service(prox_s1)
    for serv in bbs:
        print(serv.info())
        print()
    print()
    print(line_line("проверка переадресации задачи под номером 2 (preading_Troyan)",80,"="))
    print(prox_s1.info())
    print()
    print(serv_1.info())
    print()
    prox_s1.pull_task(2)
    print(prox_s1.info())
    print()
    print(serv_1.info())



if __name__ == "__main__":
    run_demo()