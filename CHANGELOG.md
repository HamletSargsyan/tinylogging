# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Updated `poetry` to version 2.0.0

## [5.0.0] - 2025-01-25

### Added

- Method `to_dict` for the `Record` class
- Documentation for project (#6)
- Typings for project

### Removed

- `COLOR_MAP` from `tinylogging/__init__.py`

## [4.2.0] - 2025-01-17

### Added

- Optional parameter `message_thread_id` for handlers `AsyncTelegramHandler` and `TelegramHandler`

## [4.1.0] - 2025-01-17

### Added

- Added emoji support for log levels in `Formatter`

### Changed

- Changed the default time format in `TelegramFormatter` from `[%H:%M:%S]` to `%H:%M:%S`

### Fixed

- Fixed an issue where messages could be displayed even when the logger was disabled

## [4.0.0] - 2025-01-14

### Added

- Handler for sending logs to Telegram (`AsyncTelegramHandler`, `TelegramHandler`) (#4)
- New formatter `TelegramFormatter` for processing and formatting messages sent to Telegram
- New dependency: `httpx` for working with the Telegram API

### Removed

- Dropped support for Python 3.8

## [3.3.0] - 2025-01-11

### Fixed

- Fixed an issue in `LoggingAdapterHandler` where the attributes `filename`, `function`, and `line` were not set for the `Record` object

### Changed

- Reorganized imports

## [3.2.0] - 2024-11-01

### Fixed

- Error in detecting stack depth (#3)

## [3.1.0] - 2024-10-31

### Added

- New attributes for the `Record` class: `filename`, `line`, `basename`, `relpath`, `function`

### Changed

- In the default template (attribute `template`) for the `Formatter` class, the relative path to the file and line are displayed

## [3.0.0] - 2024-10-13

### Added

- Asynchronous support
- New dependency: `anyio`

### Changed

- Changed structure and module imports for better code organization

## [2.2.0] - 2024-10-05

### Fixed

- Issue #2

## [2.1.0] - 2024-10-05

### Added

- `LoggingAdapterHandler`: an adapter for integration with the `logging` module allowing the use of custom handlers (`BaseHandler`, `StreamHandler`, etc.) with standard Python loggers

## [2.0.0] - 2024-10-04

### Fixed

- Issue #1

## [1.0.0] - 2024-10-04

### Added

- Initial release
