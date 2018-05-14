# encoding: utf-8
# Библиотека для упрощения логирования ошибок с помощью добавления декоратора к названию функции


import logging

class ErrorHandler():
	"""
	Библиотека для упрощения логирования ошибок с помощью добавления декоратора к названию функции. 
	Пример использования: пусть имеется функция divide_numbers, которая возвращает результат деления двух чисел. Сначала вызываем ее с аргументами 6 и 3, затем - с 6 и 0 (результат - ошибка). Для логирования работы функции divide_numbers достаточно добавить перед ней @eh.trace:

	from error_handler_decorator import ErrorHandler
	eh = ErrorHandler()

	@eh.trace
	def divide_numbers(a, b):
		return a / b

	divide_numbers(a = 6, b = 3)
	divide_numbers(6, 0)


	Результат (на экране и в файле error.log (в error.log еще добавляются служебные столбцы)):
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
	"""

	def __init__(self, logfile = 'error.log', appname = 'ErrorHandler', mode = 'a', logformat = '%(asctime)s	%(name)s	%(levelname)s	%(message)s'):
		"""
		Инициализация переменных:
		logfile - файл для записи логов с помощью библиотеки logging. По умолчанию пишет в файл error.log в папке скрипта, из которого вызвана библиотека
		appname - название приложение (по умолчанию ErrorHandler), от имени которого пишем лог в файл logfile
		mode - тип записи в файл logfile ('w' - чистим файл и пишем заново, 'a' - по умолчанию добавляем к существующему файлу)
		logformat - формат записи лога в logfile. Подробнее в таблице https://docs.python.org/3/library/logging.html#logrecord-attributes
		"""
		self.logfile = logfile

		self.logger = logging.getLogger( appname )
		self.logger.setLevel( logging.INFO )
		
		formatter = logging.Formatter( logformat )
		hdlr = logging.FileHandler( logfile, mode = mode )		
		hdlr.setFormatter( formatter )

		self.logger.addHandler( hdlr )
		

	def trace(self, func):
		"""Возвращает лог работы функции func. Для использования метода ставим перед описанием функции @ErrorHandler().trace"""

		def wrapper(*args, **kwargs):
			"""
			Формирует лог работы функции func: на экран и в файл logfile выводится информация о работе функции в формате:
			TRACE: calling название функции() with (позиционные аргументы), {именованные аргументы}

			Если в процессе выполнения декорируемой функции возникла ошибка, то ее traceback выводится на экран и пишется в logfile.
			"""

			print(f'TRACE: calling {func.__name__}() with {args}, {kwargs}')
			self.logger.info(f'TRACE: calling {func.__name__}() with {args}, {kwargs}')

			try:
				return func(*args, **kwargs)

			except Exception as e:
				print(f'ERROR: {e}. See {self.logfile} for more details')
				self.logger.exception(e)
				raise

		return wrapper


if __name__ == '__main__':
	eh = ErrorHandler()

	@eh.trace
	def divide_numbers(a, b):
		return a / b

	divide_numbers(a = 6, b = 3)
	divide_numbers(6, 0)