# Упрощение логирования ошибок с помощью добавления декоратора к названию функции

## Установка
В папке с setup.py выполните: 
```python
pip install .
```

Менее удобный вариант: в коде вашего скрипта добавьте:
```python
import sys
sys.path.append('/path/to/error_handler_decorator.py/file')
from errorhandlerdecorator import ErrorHandler
```

## Быстрый старт
Пример использования: пусть имеется функция divide_numbers, которая возвращает результат деления двух чисел. Сначала вызываем ее с аргументами 6 и 3, затем - с 6 и 0 (результат - ошибка). Для логирования работы функции divide_numbers достаточно добавить перед ней @eh.trace:

```python
from errorhandlerdecorator import ErrorHandler
eh = ErrorHandler()

@eh.trace
def divide_numbers(a, b):
	return a / b

divide_numbers(a = 6, b = 3)
divide_numbers(6, 0)
```

<b>Результат</b> (на экране и в файле error.log (в error.log еще добавляются служебные столбцы)):
```
TRACE: calling divide_numbers() with (), {'a': 6, 'b': 3}
TRACE: calling divide_numbers() with (6, 0), {}
ERROR: division by zero. See error.log for more details
Traceback (most recent call last):
  File "error_handler_examples.py", line 16, in <module>
    divide_numbers(6, 0)
  File "error-handler-decorator\error_handler_decorator.py", line 43, in wrapper

    return func(*args, **kwargs)
  File "error_handler_examples.py", line 13, in divide_numbers
    return a / b
ZeroDivisionError: division by zero
```


## Опции при инициализации ErrorHandler
При использовании библиотеки предусмотрены следующие параметры:
* logfile - файл для записи логов с помощью библиотеки logging. По умолчанию пишет в файл error.log в папке скрипта, из которого вызвана библиотека
* appname - название приложение (по умолчанию ErrorHandler), от имени которого пишем лог в файл logfile
* mode - тип записи в файл logfile ('w' - чистим файл и пишем заново, 'a' - по умолчанию добавляем к существующему файлу)
* logformat - формат записи лога в logfile. Подробнее в таблице https://docs.python.org/3/library/logging.html#logrecord-attributes


