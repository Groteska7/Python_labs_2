from src.lab01.model import Sersev
from .model import SersevList
from ..lib_file import line_line

def run_demo():
    LEN=150
    # print(line_line(row="Тестирование Sersevlist", ln=LEN, dot="="))
    print(line_line(row="Тестирование add_service и get_service", ln=LEN, dot="="))
    s1 = Sersev("MainServerOne", max_tasks=4)
    NoNoNoMrFish = Sersev("MainServerOne", max_tasks=13421)
    s2 = Sersev("MainServerTwo", max_tasks=2)
    Propopio=Sersev("Bileberda", max_tasks=6)
    print(f"Объект создан: {s1}")
    print(f"Объект создан: {s2}")
    print(f"Объект создан: {Propopio}")
    S_list=SersevList("List_one")
    print(f"Объект создан: Контейнер S_list")
    S_list.add_service(s1)
    print(S_list.__getitem__())
    S_list.add_service(s2)
    print(S_list.__getitem__())
    S_list.add_service(Propopio)
    print(S_list.__getitem__())
    S_list.add_service(NoNoNoMrFish)
    S_list.add_service(s2)
    print(f"print(S_list[2]) = {S_list[2]}")
    print(line_line(row="Тестирование __len__", ln=LEN, dot="="))
    print(len(S_list))
    print(line_line(row="Тестирование __iter__", ln=LEN, dot="="))
    for i in S_list:
        print(i)
    print(line_line(row="Тестирование find_by_name и find_by_index", ln=LEN, dot="="))
    print(f"Поиск по имени Bileberda: {S_list.find_by_name("Bileberda")}")
    print(f"Поиск по имени MainServerOne: {S_list.find_by_name("MainServerOne")}")
    print(f"Поиск по имени SuspiciousForeigner: {S_list.find_by_name("SuspiciousForeigner")}")
    print(f"Поиск по индексу 2: {S_list.find_by_index(0)}")
    print(f"Поиск по индексу 4322: {S_list.find_by_index(4322)}")
    print(line_line(row="Тестирование remove_by_name и remove_by_index", ln=LEN, dot="="))
    print(f"Удаление по имени MainServerOne:")
    {S_list.remove_by_name("MainServerOne")}
    print(S_list.__getitem__())
    print()
    print(f"Удаление по индексу 0:")
    {S_list.remove_by_index(0)}
    print(S_list.__getitem__())
    print(line_line(row="Тестирование вывода ошибок", ln=LEN, dot="="))
    print("Попытка записать в контейнер что то кроме экземпляра класса Sercev")
    S_list.add_service("NoString!")

if __name__ == "__main__":
    run_demo()



