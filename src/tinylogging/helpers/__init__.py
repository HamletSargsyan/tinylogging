import html

from tinylogging.formatter import Formatter
from tinylogging.record import Record

__all__ = [
    "TelegramFormatter",
]


class TelegramFormatter(Formatter):
    def __init__(self, time_format: str = "%H:%M:%S"):
        """
        Initializes the TelegramFormatter with a specific time format and template.

        Args:
            time_format (str): The format string for formatting the time. Defaults to "%H:%M:%S".
        """
        template = (
            "<b>{emoji} {level}</b>\n\n"
            "<b>time:</b> <code>{time}</code>\n"
            "<b>logger:</b> <code>{name}</code>\n"
            "<b>file:</b> <code>{relpath}</code>\n"
            "<b>line:</b> <code>{line}</code>\n\n"
            "<pre><code class='language-shell'>{message}</code></pre>"
        )
        super().__init__(time_format=time_format, template=template, colorize=False)

    def format(self, record: Record) -> str:
        """
        Formats a log record into a string suitable for Telegram.

        Args:
            record (Record): The log record to format.

        Returns:
            str: The formatted log record as a string.
        """
        record.message = html.escape(record.message)
        return self._format(record)
