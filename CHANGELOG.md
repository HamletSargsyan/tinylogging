# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.3.0] - 2025-01-11

### Fixed

- Исправлена проблема в `LoggingAdapterHandler`, из-за которой атрибуты `filename`, `function` и `line` не устанавливались для объекта `Record`

### Changed

- Реорганизованы импорты

## [3.2.0] - 2024-11-01

### Fixed

- Ошибка при обнаружении глубины стека (#3)

## [3.1.0] - 2024-10-31

### Added

- Новые атрибуты для класса `Record`: `filename`, `line`, `basename`, `relpath`, `function`

### Changed

- В дефолтном шаблоне (атрибут `template`) для класса `Formatter` отображаются относительный путь к файлу и строку

## [3.0.0] - 2024-10-13

### Added

- Поддержка асинхронности
- Новая зависимость: `anyio`

### Changed

- Изменена структура и импорт модулей для лучшей организации кода

## [2.2.0] - 2024-10-05

### Fixed

- Issue #2

## [2.1.0] - 2024-10-05

### Added

- `LoggingAdapterHandler`: адаптер для интеграции с модулем `logging` позволяющий использовать пользовательские обработчики (`BaseHandler`, `StreamHandler` и т. д.) со стандартными логгерами Python

## [2.0.0] - 2024-10-04

### Fixed

- Issue #1

## [1.0.0] - 2024-10-04

### Added

- Первый релиз
