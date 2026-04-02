from src.lab01.model import Sersev

class SersevList:
    def __init__(self,name:str):
        self._services=[]
        self._name=name

    def __len__(self):
        return len(self._services)
    
    def __getitem__(self,index=None):
        if index==None:
            return list(self._services)
        return self._services[index]
    
    def remove_by_name(self,name: str):
        len_start=len(self._services)
        self._services=[serv for serv in self._services if serv.name!= name]
        if len_start>len(self._services):
            print(f"сервис {name} удален")
        else:
            print(f"сервис {name} не найден")
    
    def remove_by_index(self,index: int):
        if index==str:
            raise TypeError("Индекс должен быть числом")
        len_start=len(self._services)
        try:
            self._services=[self._services[inx] for inx in range(0,len(self._services)) if inx!=index]
            if len_start>len(self._services):
                print(f"сервис с индеком {index} удален")
        except IndexError:
            return f"Сервис с индексом {index} не существует"
    
    def find_by_name(self,name:str):
        return next((serv for serv in self._services if serv.name==name),f"Элемент с именем {name} не найден")
    
    def find_by_index(self,index:int):
        if index==str:
            raise TypeError("Индекс должен быть числом")
        try:
            return self._services[index]
        except IndexError:
            return f"Сервис с индексом {index} не существует"

    def add_service(self,service):
        if not isinstance(service,Sersev):
            raise TypeError(f"{service} не является экземпляром класса Sersev")
        elif any(s.name == service.name for s in self._services):
            if any(s == service for s in self._services):
                print(f"Сервис с именем {service.name} является жалкой породией")
            else:
                print(f"Сервис {service.name} уже добавлен")
        else:
            self._services.append(service)

    def __iter__(self):
        return iter(self._services)
    
    
    def __repr__(self):
        return f"SersevList(name='{self._name}', count={len(self._services)})"
        