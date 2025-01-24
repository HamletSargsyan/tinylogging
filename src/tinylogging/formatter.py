from colorama import Fore, Style

from tinylogging.level import Level
from tinylogging.record import Record

__all__ = ["Formatter"]


class Formatter:
    def __init__(
        self,
        time_format: str = "[%H:%M:%S]",
        template: str = "{time} | {level} | {relpath}:{line} | {message}",
        colorize: bool = True,
    ) -> None:
        """
        Initializes the Formatter instance.

        Args:
            time_format (str): The format for the timestamp in log messages.
            template (str): The template for formatting log messages.
            colorize (bool): Whether to colorize the log messages.
        """
        self.template = template
        self.time_format = time_format
        self.colorize = colorize
        self.color_map: dict[Level, str] = {
            Level.TRACE: Fore.WHITE + Style.DIM,
            Level.DEBUG: Fore.CYAN,
            Level.INFO: Fore.BLUE,
            Level.NOTICE: Fore.MAGENTA,
            Level.WARNING: Fore.LIGHTYELLOW_EX,  # cspell: disable-line
            Level.ERROR: Fore.LIGHTRED_EX,  # cspell: disable-line
            Level.CRITICAL: Fore.RED + Style.BRIGHT,
        }
        self.emojis: dict[Level, str] = {
            Level.TRACE: "🧐",
            Level.DEBUG: "🐛",
            Level.INFO: "💡",
            Level.NOTICE: "📌",
            Level.WARNING: "⚠️",
            Level.ERROR: "🚨",
            Level.CRITICAL: "💥",
        }

    def format(self, record: Record) -> str:
        """
        Formats a log record.

        Args:
            record (Record): The log record to format.

        Returns:
            str: The formatted log message.
        """
        formatted_text = self._format(record)

        if self.colorize:
            color = self.color_map.get(record.level, "")
            return f"{color}{formatted_text}{Style.RESET_ALL}\n"
        return formatted_text + "\n"

    def _format(self, record: Record) -> str:
        """
        Internal method to format a log record based on the template.

        Args:
            record (Record): The log record to format.

        Returns:
            str: The formatted log message.
        """
        return self.template.format(
            level=record.level.name,
            message=record.message,
            time=record.time.strftime(self.time_format),
            name=record.name,
            filename=record.filename,
            line=record.line,
            basename=record.basename,
            relpath=record.relpath,
            function=record.function,
            emoji=self.emojis.get(record.level, ""),
        )
