
# **🌟 Log Generator 3000 (LG3K)**

<p align="center">
  <img src="logo.png.png" alt="LG3K Logo" width="400">
</p>

<p align="center">
  <b>🚀 The ultimate modular log generation tool, designed for modern systems! 🌍</b>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://github.com/mikl0s/LG3K"><img src="https://img.shields.io/github/stars/mikl0s/LG3K.svg" alt="Stars"></a>
  <a href="https://github.com/mikl0s/LG3K/issues"><img src="https://img.shields.io/github/issues/mikl0s/LG3K.svg" alt="Issues"></a>
  <a href="https://github.com/mikl0s/LG3K/actions"><img src="https://img.shields.io/github/actions/workflow/status/mikl0s/LG3K/ci.yml" alt="Build Status"></a>
</p>

---

## **About**

Welcome to **Log Generator 3000**—a fully modular log generation tool designed to simplify testing and monitoring across diverse systems. It supports web servers, APIs, databases, firewalls, and more.

This project was conceptualized, developed, and published entirely on an iPad during a Saturday evening of football—and yes, the team we were rooting for won! 🎉

Curious about the full story? [Read more here](./about_log_generator.md).

---

## **📂 Project Structure**

```
log_generator/
├── main.py               # The entry point for the program
├── modules/              # Folder containing all log generation modules
│   ├── web_server.py     # Module for web server logs
│   ├── database.py       # Module for database logs
│   ├── api.py            # Module for API logs
│   ├── firewall.py       # Module for firewall logs
│   ├── nas.py            # Module for NAS logs
│   ├── os.py             # Module for OS logs
│   ├── network.py        # Module for network logs
│   ├── printer.py        # Module for printer logs
├── utils/                # Folder containing utility functions
│   ├── config.py         # Utilities for configuration handling
│   ├── progress.py       # Utilities for progress and threading
│   ├── timestamp.py      # Timestamp generation utilities
```

---

## **✨ Features**

- **Dynamic Module Loading**: Easily add new log types by creating a module in the `modules/` folder.
- **Scalable and Modular**: Keep your codebase clean and maintainable by separating log logic into distinct files.
- **Rich UI**: Enjoy a beautiful, real-time progress bar for generating logs (or use `--simple` mode for minimal output).
- **Fully Configurable**: Modify the configuration file to control active services, total logs, threading, and more.

---

## **🚀 Getting Started**

### **Prerequisites**
- Python 3.7 or later
- Optional: `rich` for advanced UI:
  ```bash
  pip install rich
  ```

---

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mikl0s/LG3K.git
   cd LG3K
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program:**
   ```bash
   python main.py
   ```

---

## **📦 Adding New Modules**

Adding a new log type is as simple as creating a new file in the `modules/` folder. Each module should expose a `generate_log()` function. For example:

**modules/custom_logs.py**
```python
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    return {
        "timestamp": timestamp,
        "level": level,
        "component": "CustomLogs",
        "message": "Custom log entry generated.",
    }
```

The main program will automatically detect and use this new module.

---

## **🔧 Configuration**

The configuration file (`config.json`) controls the active services, total logs, split size, and threading. If the file does not exist, it will be created with default values:

```json
{
    "services": ["web_server"],
    "total_logs": 1000,
    "split_size": 100,
    "max_threads": 4
}
```

Modify the `services` list to include the desired modules (e.g., `["web_server", "custom_logs"]`).

---

## **📊 Sample Output**

### **Rich UI (Default Mode)**

```text
[Thread 1] ██████▉ 90% (90/100 logs)
[Thread 2] ████████▌ 100% (100/100 logs) Completed: logs_part2.json
...
```

### **Simple Mode**
```text
Starting log generation for 1000 logs across 10 files.
Thread 1 completed generating ./logs/logs_part1.json
Thread 2 completed generating ./logs/logs_part2.json
...
```

---

## **🌟 Contribution**

We ❤️ contributions! Add new modules or enhance the existing ones by following these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## **📜 License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **💬 Questions?**

Feel free to open an issue or contact us at `support@loggenerator3000.com`.

---

## **🌌 Show Your Support**

If you love **Log Generator 3000**, give us a ⭐ on GitHub! Spread the word and help others test their systems with ease.