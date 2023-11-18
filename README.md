# PON/2

## English

PON/2 - it's JSON with Python types and support for custom classes.

### Changes from JSON

```json
{
  # Comments here start like in python
"PON2": True, # Boolean types as in python: True, False
"json": False,
"str": "str",
"Nothing": None, # Instead of null from json, None from python
0: "0", # Keys can be any basic types (int, str, bool, None, etc.), as well as custom types and types - (set, frozenset, list, tuple, etc.)
tuple: (tuple([1]), (1, 1, )), # Support for tuples and functions for calling them.
list: [list([1]), [1]], # Lists and functions for calling them
dict: [{"key": "value"}, dict(key="value", )], # dict ONLY supports hashable types as a KEY
set: [set([1, 2, 3]), {1, 2, 3}], #Set supported
frozenset: frozenset(), # frozenset are supported via the function
"numbers": [1, 1.0, 0x1, 0o1, 0b1], # support for int, float, hex, octal, binary numbers
"callables": [
# Callable types
str(0),
int(0),
bool(0),
float(0),
dict(k=0),
list([0]),
tuple([0]),
set([0]),
frozenset([0])
]
}
```
## Документация

PON is similar to the JSON module, but is based on the PONLoader class.
```python
import pon2
>> > pon2.loader.load(open("test.pon"))
{"file": ("tuple", "t")}
>> > pon2.loader.loads("""{"file": ("tuple", "t")}""")
{"file": ("tuple", "t")}
```

### Custom Types

```python
from pon2 import PONLoader, NamespaceDict


class Custom:
    def __init__(self, value: int, v2: int):
        self.value = value
        self.v2 = v2

    def __str__(self):
        return f"Custom(value={self.value}, v2={self.v2})"

    def __repr__(self):
        return self.__str__()


custom_loader = PONLoader(NamespaceDict({Custom}))
data = str({"Data": Custom(10, 15)})
>> > print(data)
"""{"Data": Custom(value=10, v2=15)}"""
>> > print(custom_loader.loads(data))
{"Data": Custom(value=10, v2=15)}
```


## Русский

PON/2 - это JSON с python-типами и поддержкой custom-классов.

### Изменения по сравнению с JSON

```json
{
  # Комментарии тут начинаются как в python
"PON2": True, # Булевые типы как в python: True, False
"json": False,
"str": "str",
"Nothing": None, # Вместо null из json, None из python
0: "0", # Ключами могут быть любые базовые типы(int, str, bool, None), а также кастомные типы и типы - (set, frozenset, list, tuple и тд)
tuple: (tuple([1]), (1, 1, )), # Поддержка кортежей и функций их вызова.
list: [list([1]), [1]], # Списки и функции их вызова
dict: [{"key": "value"}, dict(key="value", )], # dict поддерживает ТОЛЬКО хешируемые типы в качестве КЛЮЧА
set: [set([1, 2, 3]), {1, 2, 3}], # Set поддерживается
frozenset: frozenset(), # frozenset поддерживаются через функцию
"numbers": [1, 1.0, 0x1, 0o1, 0b1], # поддержка чисел int, float, hex, octal, binary
"callables": [
# Вызываемые типы
str(0),
int(0),
bool(0),
float(0),
dict(k=0),
list([0]),
tuple([0]),
set([0]),
frozenset([0])
]
}
```

## Документация

PON похож на JSON модуль, но работает на основе класса PONLoader

```python
import pon2
>> > pon2.loader.load(open("test.pon"))
{"file": ("tuple", "t")}
>> > pon2.loader.loads("""{"file": ("tuple", "t")}""")
{"file": ("tuple", "t")}
```

### Custom Types

```python
from pon2 import PONLoader, NamespaceDict


class Custom:
    def __init__(self, value: int, v2: int):
        self.value = value
        self.v2 = v2

    def __str__(self):
        return f"Custom(value={self.value}, v2={self.v2})"

    def __repr__(self):
        return self.__str__()


custom_loader = PONLoader(NamespaceDict({Custom}))
data = str({"Data": Custom(10, 15)})
>> > print(data)
"""{"Data": Custom(value=10, v2=15)}"""
>> > print(custom_loader.loads(data))
{"Data": Custom(value=10, v2=15)}
```
