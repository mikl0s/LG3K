# **🌟 Log Generator 3000 (LG3K)**

<p align="center">
  <img src="https://raw.githubusercontent.com/mikl0s/LG3K/main/logo.png" alt="LG3K Logo - AI generated and AI background removal to make it transparent" width="700">
</p>

<h2 align="center">🚀 The ultimate modular log generation tool, designed for modern systems! 🌍</h1>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/mikl0s/LG3K"><img src="https://img.shields.io/github/stars/mikl0s/LG3K.svg?style=for-the-badge" alt="Stars"></a>
  <a href="https://github.com/mikl0s/LG3K/issues"><img src="https://img.shields.io/github/issues/mikl0s/LG3K.svg?style=for-the-badge" alt="Issues"></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/lg3k/"><img src="https://img.shields.io/badge/pypi-v0.7.0-blue?style=for-the-badge" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/lg3k/"><img src="https://img.shields.io/badge/downloads-0-blue?style=for-the-badge" alt="PyPI Downloads"></a>
  <a href="https://pypi.org/project/lg3k/"><img src="https://img.shields.io/badge/python-3.12-blue?style=for-the-badge" alt="Python Versions"></a>
</p>

<p align="center">
  <a href="https://black.readthedocs.io/"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge" alt="Code Style: Black"></a>
  <a href="https://flake8.pycqa.org/"><img src="https://img.shields.io/badge/linter-flake8-blue.svg?style=for-the-badge" alt="Linter: Flake8"></a>
  <a href="https://pycqa.github.io/isort/"><img src="https://img.shields.io/badge/imports-isort-white.svg?style=for-the-badge" alt="Imports: isort"></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/tests-pytest-blue.svg?style=for-the-badge" alt="Tests: pytest"></a>
</p>

<p align="center">
  <a href="https://github.com/mikl0s/LG3K/commits/main"><img src="https://img.shields.io/github/last-commit/mikl0s/LG3K.svg?style=for-the-badge" alt="Last Commit"></a>
  <a href="https://github.com/mikl0s/LG3K"><img src="https://img.shields.io/github/repo-size/mikl0s/LG3K?style=for-the-badge" alt="Repo Size"></a>
  <a href="https://github.com/mikl0s/LG3K/tree/main/docs"><img src="https://img.shields.io/badge/docs-sphinx-blue.svg?style=for-the-badge" alt="Documentation"></a>
  <a href="https://github.com/mikl0s/LG3K/actions"><img src="https://img.shields.io/codecov/c/github/mikl0s/LG3K?style=for-the-badge" alt="Coverage"></a>
  <a href="https://github.com/mikl0s/LG3K/actions"><img src="https://img.shields.io/github/actions/workflow/status/mikl0s/LG3K/ci.yml?style=for-the-badge" alt="CI"></a>
</p>

---

## **Documentation Guides**

### **[Log Generation Guide](docs/log_generation_guide.md)**
Comprehensive guide for generating logs with LG3K:
- Log format specifications
- Module-specific examples
- Error handling patterns
- Progress tracking
- Best practices for log generation

### **[Llama Training How-To](docs/llama_training_howto.md)**
Step-by-step guide for training `llama3.2:3b-instruct-fp16` with LG3K logs:
- Hardware and software requirements
- Environment setup for Windows, macOS, and Ubuntu
- Training data generation
- Model configuration
- Training script implementation
- Monitoring and troubleshooting
- Memory optimization for 8-12GB VRAM GPUs

### **[Developer Guide](docs/developer_guide.md)**
Detailed guide for developers integrating LG3K:
- Configuration file management
- Programmatic usage examples
- Error handling strategies
- Progress tracking implementation
- File cleanup patterns
- Module-specific integrations
- JSON output handling
- LLM format generation

---

## **Installation**

### **From PyPI (Recommended)**

The easiest way to install LG3K is from PyPI:

```bash
pip install lg3k
```

This will install the latest stable version with all required dependencies.

### **From Source (Development)**

For the latest development version or contributing:

```bash
git clone https://github.com/mikl0s/LG3K.git
cd LG3K
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
```

### **Requirements**

- Python (latest stable version)
- Dependencies are automatically installed with pip
- Optional: `rich` package for enhanced display
- Optional: `torch` and `psutil` for GPU-optimized LLM training

---

## **About**

Welcome to **Log Generator 3000**—a fully modular log generation tool designed to simplify testing and monitoring across diverse systems. It supports web servers, APIs, databases, firewalls, and more, with special support for LLM training data generation.

This project was conceptualized, developed, and published entirely on an iPad during a Saturday evening of football—and yes, the team we were rooting for won! 🎉

Curious about the full story? [Read more here](about_log_generator_v0.1.0.md).

---

## **Contributing**

We believe in the power of community! LG3K becomes more valuable with each new contribution, whether it's adding new log types, improving existing ones, or enhancing the core functionality.

### **Ways to Contribute**

1. **Add New Log Types** 📝
   - Create new modules for different systems
   - Enhance existing log formats
   - Add more realistic log patterns

2. **Improve Core Features** 🛠️
   - Enhance performance
   - Add new configuration options
   - Improve error handling

3. **Documentation** 📚
   - Improve documentation
   - Add examples
   - Write tutorials

4. **Testing** 🧪
   - Add unit tests
   - Report bugs
   - Suggest improvements

### **Getting Started with Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements-dev.txt  # Installs all development dependencies
   pip install -e .  # Install package in development mode
   pre-commit install
   ```
4. Run tests:
   ```bash
   pytest  # Runs tests with coverage report
   ```
5. Make your changes (the pre-commit hooks will ensure code quality)
6. Write tests if applicable
7. Update documentation if needed
8. Commit your changes (`git commit -m 'Add feature'`)
9. Push to your branch (`git push origin feature-name`)
10. Open a Pull Request

### **Development Guidelines**

- Code is formatted with Black (88 characters line length)
- Imports are sorted with isort
- Code quality is checked with Flake8
- All functions and modules have docstrings
- Changes are covered by tests (when applicable)

---

## **📂 Project Structure**

```
lg3k/
├── __init__.py          # Package initialization
├── modules/             # Folder containing all log generation modules
│   ├── web_server.py    # Module for web server logs
│   ├── database.py      # Module for database logs
│   ├── api.py           # Module for API logs
│   ├── firewall.py      # Module for firewall logs
│   ├── nas.py           # Module for NAS logs
│   ├── os.py            # Module for OS logs
│   ├── network.py       # Module for network logs
│   ├── printer.py       # Module for printer logs
│   ├── smarthome.py     # Module for smart home devices and IoT
├── utils/               # Folder containing utility functions
│   ├── config.py        # Utilities for configuration handling
│   ├── progress.py      # Utilities for progress and threading
│   ├── timestamp.py     # Timestamp generation utilities
```

---

## **✨ Features**

- **Dynamic Module Loading**: Easily add new log types by creating a module in the `modules/` folder.
- **Scalable and Modular**: Keep your codebase clean and maintainable by separating log logic into distinct files.
- **Docker-Style Progress**: Real-time progress tracking with Docker-like display for each module.
- **Smart Home Support**: Generate logs for IoT devices, ESP32/ESP8266, Zigbee/Z-Wave, and security cameras.
- **High Volume**: Generate up to 1,000,000 log entries per module.
- **Rich UI**: Beautiful, real-time progress bar for generating logs (with fallback to simple mode).
- **Fully Configurable**: Modify the configuration file to control active services, total logs, threading, and more.
- **JSON Output Mode**: Get structured output in JSON format for easy parsing and automation.
- **Configuration Generation**: Generate default configuration files with `--generate-config`.
- **Code Quality**: Enforced by Black, isort, and Flake8 through pre-commit hooks.
- **94% Test Coverage**: Comprehensive test suite ensuring reliability.
- **LLM Training Format**: Generate logs in a format optimized for training Large Language Models.
- **Rich-Free Operation**: Can run without the `rich` package installed using `--simple` or `--llm` options.
- **Graceful Error Handling**: Comprehensive error handling with informative messages.
- **Progress Status**: Real-time status updates for each module (Running, Complete, Error, Cancelled).
- **File Cleanup**: Automatic cleanup of generated files with keep-files option.
- **Module Analysis**: Built-in log analysis capabilities for each module type.

---

## **Getting Started**

### **Prerequisites**
- Python (latest stable version)
- For users:
  ```bash
  pip install -r requirements.txt
  ```
- For developers:
  ```bash
  pip install -r requirements-dev.txt
  pip install -e .
  pre-commit install
  ```

---

### **Quick Start**

1. **Install the package:**
   ```bash
   pip install lg3k
   ```

2. **Generate logs:**
   ```bash
   lg3k --count 1000 --threads 4
   ```

3. **Generate logs without rich UI:**
   ```bash
   lg3k --count 1000 --threads 4 --simple
   ```

4. **Generate logs in LLM format:**
   ```bash
   lg3k --count 1000 --threads 4 --llm-format
   ```

5. **View help:**
   ```bash
   lg3k --help
   ```

---

### **Generating Logs for LLM Training**

To generate logs in a format suitable for training Large Language Models:

```bash
lg3k --llm-format
```

This will:
- Generate logs in instruction-tuning format
- Include detailed analysis for each log entry
- Structure data for easy model training
- Support both string and JSON log formats
- Handle errors gracefully with informative messages

For more details, see the [Llama Training How-To](docs/llama_training_howto.md).

---

### **Developer Guide**

Looking to integrate LG3K into your application or AI model? Check out our [Developer Guide](docs/developer_guide.md) for:

- 🔧 Programmatic usage examples
- 🤖 AI integration patterns
- 📊 Log format specifications
- ⚡ Performance optimization tips
- 🧪 Integration testing strategies
- 🛠️ Configuration file generation
- 📋 JSON output mode usage
- 🎯 Error handling best practices
- 📈 Progress tracking implementation
- 🧹 File cleanup strategies

---

### **Available Modules**

- **Infrastructure**
  - `web_server` - Web server access logs
  - `database` - Database operations
  - `api` - API endpoint logs
  - `firewall` - Security events
  - `nas` - Storage operations
  - `os` - System logs
  - `network` - Network traffic
  - `printer` - Print jobs

- **Smart Home & IoT**
  - Smart home devices (thermostats, lights, sensors)
  - ESP32/ESP8266 microcontrollers
  - Zigbee/Z-Wave devices
  - Security cameras and doorbells

---

## **📊 Sample Output**

### **Docker-Style Progress Display**

```text
1ff5d2e3: web_server   [=========>  ] 50.0%
5520ebfb: database     [==========] Complete
e9c8c5d6: api         [>         ] Waiting
7a1b3c4d: smarthome   [=======>   ] 35.0%
...
```

### **Rich UI (Default Mode)**

```text
[Thread 1] ██████▉ 90% (90/100 logs)
[Thread 2] █████████▌ 100% (100/100 logs) Completed: logs_part2.json
...
```

### **Simple Mode**
```text
Starting log generation for 1000 logs across 10 files.
Thread 1 completed generating ./logs/logs_part1.json
Thread 2 completed generating ./logs/logs_part2.json
...
```

### **JSON Output Mode**

Use the `--json` flag for structured output in a single line (ideal for parsing):

```bash
lg3k --count 1000 --threads 4 --json
```

This outputs a single line of JSON with detailed information (formatted here for readability):

```json
{
    "success": true,
    "logs_generated": 1000,
    "time_taken": 1.23,
    "files": ["logs/part1.json", "logs/part2.json"],
    "stats": {
        "total_files": 2,
        "avg_logs_per_file": 500,
        "total_size_bytes": 12345
    },
    "timing": {
        "start_time": "2024-03-22T12:34:56.789012",
        "duration_seconds": 1.23,
        "logs_per_second": 813.0
    },
    "config": {
        "output_directory": "logs",
        "file_format": ".json"
    }
}
```

In case of errors (also single-line output):
```json
{
    "success": false,
    "logs_generated": 0,
    "time_taken": 0.0,
    "files": [],
    "error": {
        "message": "Error message here",
        "type": "ErrorType"
    }
}
```

---

## **📜 License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **💬 Questions?**

Feel free to open an issue or contact us at `lg3k@dataloes.dk`.

---

## **🌌 Show Your Support**

If you love **Log Generator 3000**, give us a ⭐ on GitHub! Spread the word and help others test their systems with ease.
