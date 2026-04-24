from ..lab01.model import Sersev
from ..lab02.collection import SersevList


class ComputeServer(Sersev):
    def __init__(self, name, cpu_power = 0.5, max_tasks = 10):
        super().__init__(name, max_tasks)
        self._cpu_power = cpu_power # [задачи в секунду]
        # self._predicted_time = len(self._tasks)//self._cpu_power
    
    @property
    def _predicted_time(self):
        return len(self._tasks)//self._cpu_power
    
    def get_estimated_time(self):
        if self._cpu_power > 0:
            return self._predicted_time
        else:
            return "задач нету, отдахаем!"
    
    def get_detailed_report(self):
        base_info = super().get_detailed_report()
        return f"[COMPUTE NODE]\n{base_info}\nМощность CPU: {self._cpu_power}"

    def set_maintenance(self):
        print(f"Остановка вычислений на {self._name}...")
        super().set_maintenance()
    
    def __str__(self):
        return f"Вычислительный сервер {self._name} [{self._status.value}] мощностью {self._cpu_power} задачь в секуду"

    def info(self):
        task_col = "\n".join(self._tasks)
        return f"Имя: сервер {self._name}\nстатус: [{self._status.value}]\nобщая мощность: {self._cpu_power}\nпронозируемое время: {self._predicted_time} c.\nзадачи:\n{task_col}"
    
    # def update(self,new_power = None):



class StorageServer(Sersev):
    def __init__(self, name, all_memory=40):
        super().__init__(name)
        self._max_tasks = all_memory//4
        self._all_memory = all_memory
        # self._use_memory = all_memory-(len(self._tasks)*4)# 1 задача = 4 байт
    
    @property
    def _use_memory(self):
        return len(self._tasks) * 4

    def get_detailed_report(self):
        return f"[STORAGE NODE] {self._name}\nДоступно памяти: {self._all_memory} байт"

    def set_maintenance(self):
        print(f"Синхронизация файловой системы {self._name} перед обслуживанием...")
        super().set_maintenance()

    def __str__(self):
        return f"Сервер с большой памятью и красивыми глазами ораньживого цвета {self._name} [{self._status.value}] с памятью {self._all_memory} байт"
    
    def info(self):
        task_col = "\n".join(self._tasks)
        return f"Имя: сервер {self._name}\nстатус: [{self._status.value}]\nобщая память: {self._all_memory}\nзаполнен на: {(self._use_memory/self._all_memory)*100}%\nзадачи:\n{task_col}"


class ProxyServer(Sersev):
    def __init__(self, name, max_tasks = 10, ping = 30, target_server: Sersev = None):
        super().__init__(name, max_tasks)
        self._ping = ping
        self._target_server = target_server
        if not isinstance(self._target_server,Sersev) and self._target_server != None:
            raise TypeError (f"Целевой сервер должен быть сервером")
    
    def take_target(self,target):
        if not isinstance(target,Sersev):
            raise TypeError (f"Целевой сервер должен быть сервером")
        else:
            self._target_server=target

    def pull_task(self,num:int):
        if self._target_server.max_tasks<=len(self._target_server._tasks):
            raise BufferError(f"сервер {self._target_server._name} переполнен.")
        else:
            task=self._tasks.pop(num)
            self._target_server.add_task(task)
            return f"задача перенаправлена на {self._target_server._name}."

    def __str__(self):
        return f"Плей бой, филантроп, всемизвестный прокси сервер {self._name} [{self._status.value}] с задержкой {self._ping} мс"
    
    def set_maintenance(self):
        self._target_server = None
        self._status = self.ServiceStatus.MAINTENANCE
        print(f"Север {self._name} переведен на тех. обслуживание.")
    
    def info(self):
        task_col = "\n".join(self._tasks)
        return f"Имя: сервер {self._name}\nзадержка: {self._ping} мс\nконечный сервер {self._target_server.name}\nзадачи:\n{task_col}"