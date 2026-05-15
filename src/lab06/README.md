# Лабораторная работа №6

## Цель работы
Освоить систему аннотаций типов в Python, научиться создавать обобщённые (generic) классы с помощью `TypeVar` и `Generic`, понять концепцию структурной типизации через `Protocol`.

## Что добавлено и изменено

### Аннотации типов
- Все классы в `lab01/model.py` имеют аннотации типов
- Добавлены методы `display() -> str` и `score() -> float`

### Класс TypedCollection[T]
Обобщённая коллекция, заменившая коллекцию из ЛР-2:

- `add()`, `remove()`, `get_all()`
- `find_by_name()`, `find_by_index()`
- `remove_by_name()`, `remove_by_index()`
- `get_only_type()`
- `__len__`, `__getitem__`, `__iter__`
- `find(predicate)` — поиск элемента по условию
- `filter(predicate)` — фильтрация элементов
- `map(transform)` — преобразование с изменением типа

### Протоколы и ограничения
- `Displayable(Protocol)` — требует метод `display() -> str`
- `Scorable(Protocol)` — требует метод `score() -> float`
- `TypedCollection[D]` — для объектов с методом `display()`
- `TypedCollection[S]` — для объектов с методом `score()`

## Демонстрация работы

### TypedCollection — базовое использование
![i1](/images/lab06/img1.png)
### find(), filter(), map()
![i2](/images/lab06/img2.png)
### TypedCollection[D] — протокол Displayable
![i3](/images/lab06/img3.png)
### TypedCollection[S] — протокол Scorable
![i4](/images/lab06/img4.png)

![codic](https://i.pinimg.com/736x/4e/c5/62/4ec56262a001f599d5f470d21608f892.jpg)