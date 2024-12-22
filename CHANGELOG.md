# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.3] - 2024-03-22

### Added
- Smart home device support
  - Thermostats, lights, sensors, locks
  - ESP32/ESP8266 microcontrollers
  - Zigbee/Z-Wave devices
  - Security cameras and doorbells
- Docker-style progress display
  - Unique module IDs
  - Real-time progress tracking
  - Better status display
- PyPI package distribution
  - Published to PyPI (`pip install lg3k`)
  - Improved package metadata
  - Proper classifiers and dependencies

### Fixed
- Wireless device tests for protocol-specific network IDs
- Test coverage improved to 100%

### Changed
- Updated Python requirement to 3.12
- Improved package structure
- Enhanced documentation

## [0.6.2] - 2024-03-22

### Fixed
- Protocol-specific network ID handling in wireless device tests

## [0.6.1] - 2024-03-22

### Added
- Smart home module documentation
- Progress display examples

## [0.6.0] - 2024-03-22

### Added
- Initial release with core features
- Multi-threaded log generation
- Multiple log types support
- Rich TUI interface
