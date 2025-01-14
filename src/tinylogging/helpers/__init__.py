import html

from tinylogging.formatter import Formatter
from tinylogging.record import Record

__all__ = [
    "TelegramFormatter",
]


class TelegramFormatter(Formatter):
    def __init__(self, time_format: str = "[%H:%M:%S]"):
        template = (
            "<b>{level}</b>\n\n"
            "<b>time:</b> <code>{time}</code>\n"
            "<b>logger:</b> <code>{name}</code>\n"
            "<b>file:</b> <code>{relpath}</code>\n"
            "<b>line:</b> <code>{line}</code>\n\n"
            "<pre><code class='language-shell'>{message}</code></pre>"
        )
        super().__init__(time_format=time_format, template=template, colorize=False)

    def format(self, record: Record):
        record.message = html.escape(record.message)
        return self._format(record)
