# tinylogging

![GitHub License](https://img.shields.io/github/license/HamletSargsyan/tinylogging)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/HamletSargsyan/tinylogging)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tinylogging)
![PyPI - Version](https://img.shields.io/pypi/v/tinylogging)
![Checks](https://github.com/HamletSargsyan/tinylogging/actions/workflows/check.yml/badge.svg)

## Установка

```bash
pip install tinylogging
```

## Использование

### Создание нового логгера

```python
from tinylogging import Logger, Level

logger = Logger(name="my_logger", level=Level.DEBUG)

```

### Логирование сообщений

```python
logger.info("This is an info message.")
logger.error("This is an error message.")
logger.debug("This is a debug message.")
```

### Логирования в файл

```python
from tinylogging import FileHandler

file_handler = FileHandler(file_name="app.log", level=Level.WARNING)
logger.handlers.add(file_handler)

logger.warning("This warning will be logged to both console and file.")
```

### Пользовательское форматирование

```python
from tinylogging import Formatter

formatter = Formatter(template="{time} - {name} - {level} - {message}", colorize=False)
logger = Logger(name="custom_logger", formatter=formatter)
logger.info("This log message uses a custom format.")
```

### Отключение логирования

```python
logger.disable()
logger.info("This message will not be logged.")
logger.enable()
```

### Поддержка асинхронности

```python
import anyio
from tinylogging import AsyncLogger, AsyncFileHandler


async def main():
    logger = AsyncLogger(name="async_logger")

    file_handler = AsyncFileHandler(file_name="app.log")
    logger.handlers.add(file_handler)

    await logger.info("This is an info message.")
    await logger.error("This is an error message.")
    await logger.debug("This is a debug message.")


if __name__ == "__main__":
    anyio.run(main)
```

## Лицензия

Этот проект лицензирован под лицензией [MIT](https://github.com/HamletSargsyan/tiny-logging/blob/main/LICENSE).
