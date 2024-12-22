# LG3K Developer Guide

## Quick Installation

```bash
pip install lg3k
```

## Configuration File

### Overview
LG3K uses a JSON configuration file to control its behavior. The configuration file specifies which log generators to use, how many logs to generate, and how many threads to use for parallel generation.

### Generating a Configuration File
You can generate a default configuration file using the `--generate-config` option:

```bash
lg3k --generate-config config.json
```

This will create a configuration file with default settings. The generated file will include:
- A list of all available log generators
- Default log count settings
- Default thread count settings

### Configuration File Structure
```json
{
    "services": [
        "api",
        "database",
        "firewall",
        "nas",
        "network",
        "os",
        "printer",
        "web_server",
        "smarthome"
    ],
    "count": 100,
    "threads": 4
}
```

### Configuration Options

#### services
- Type: Array of strings
- Description: List of log generators to use
- Available options:
  - `api`: API endpoint logs
  - `database`: Database operation logs
  - `firewall`: Security logs
  - `nas`: Network storage logs
  - `network`: Network traffic logs
  - `os`: Operating system logs
  - `printer`: Print job logs
  - `web_server`: Web server access logs
  - `smarthome`: Smart home device logs

#### count
- Type: Integer
- Description: Number of log entries to generate per service
- Default: 100
- Maximum: 1,000,000

#### threads
- Type: Integer
- Description: Number of threads to use for parallel log generation
- Default: System CPU count
- Minimum: 1

### Using the Configuration File
Once you have a configuration file, you can use it with LG3K:

```bash
lg3k --config config.json
```

You can override configuration file settings using command-line options:

```bash
lg3k --config config.json --count 1000 --threads 2
```

## Programmatic Usage

### Basic Import and Setup

```python
from lg3k.modules import (
    api,           # API endpoint logs
    database,      # Database operations
    firewall,      # Security events
    nas,          # Storage operations
    network,      # Network traffic
    os,           # System logs
    printer,      # Print jobs
    smarthome,    # IoT and smart home logs
    web_server,   # Web server access logs
)

# Each module provides a generate_log() function
log_entry = api.generate_log()
print(log_entry)
```

### Programmatic Output Mode

When using LG3K in scripts or automated workflows, you can use the `--json` flag to get a single-line JSON output that's easy to parse:

```bash
lg3k --count 1000 --threads 4 --json
```

This will output a single line with a JSON object containing:
```json
{
    "success": true,
    "logs_generated": 1000,
    "time_taken": 1.23,
    "files": ["logs/part1.json", "logs/part2.json"]
}
```

The process will exit with:
- Code 0: Success
- Code 1: Error (with error details in the JSON output)

### Batch Generation

```python
def generate_batch(module, count=1000):
    """Generate a batch of logs from a specific module."""
    return [module.generate_log() for _ in range(count)]

# Generate 1000 API logs
api_logs = generate_batch(api)

# Generate logs from multiple modules
modules = [api, database, web_server]
all_logs = []
for module in modules:
    all_logs.extend(generate_batch(module, count=100))
```

### Smart Home Specific Usage

```python
# Generate different types of smart home logs
device_log = smarthome.generate_log()              # General smart home log
home_device = smarthome.generate_home_device_log() # Thermostat, light, sensor
esp_log = smarthome.generate_esp_log()            # ESP32/ESP8266 log
wireless = smarthome.generate_wireless_log()       # Zigbee/Z-Wave log
camera = smarthome.generate_camera_log()          # Security camera log
```

## AI Integration Examples

### Context Generation for LLMs

```python
def generate_training_context(modules, logs_per_module=100):
    """Generate a context dictionary suitable for LLM training."""
    context = {}
    for module in modules:
        module_name = module.__name__.split('.')[-1]
        logs = generate_batch(module, logs_per_module)
        context[module_name] = {
            'logs': logs,
            'format': module.__doc__,  # Module documentation
            'example': logs[0]         # Example log entry
        }
    return context

# Generate context for specific modules
training_context = generate_training_context([api, database])
```

### Log Analysis Training Data

```python
def generate_analysis_dataset(anomaly_ratio=0.1):
    """Generate a labeled dataset for log analysis training."""
    normal_logs = generate_batch(web_server, 1000)
    # Modify some logs to create anomalies
    anomaly_logs = [
        log.replace('200', '500')
        for log in generate_batch(web_server, int(1000 * anomaly_ratio))
    ]

    dataset = []
    for log in normal_logs:
        dataset.append({'log': log, 'label': 'normal'})
    for log in anomaly_logs:
        dataset.append({'log': log, 'label': 'anomaly'})

    return dataset
```

### Real-time Stream Simulation

```python
import time
import random

def simulate_log_stream(modules, delay_range=(0.1, 0.5)):
    """Simulate a real-time log stream for testing."""
    while True:
        module = random.choice(modules)
        log = module.generate_log()
        yield {
            'timestamp': time.time(),
            'module': module.__name__,
            'log': log
        }
        time.sleep(random.uniform(*delay_range))

# Usage in async context
async def process_log_stream():
    modules = [api, database, web_server]
    async for log_entry in simulate_log_stream(modules):
        # Process log entry
        await process_log(log_entry)
```

## Log Formats

Each module generates logs in a specific format. Here are some examples:

### API Logs
```python
{
    'timestamp': '2024-03-22T15:30:45Z',
    'method': 'POST',
    'endpoint': '/api/v1/users',
    'status': 201,
    'response_time': 45,
    'client_ip': '192.168.1.100'
}
```

### Smart Home Logs
```python
{
    'timestamp': '2024-03-22T15:30:45Z',
    'device_type': 'thermostat',
    'device_id': 'THERM001',
    'event': 'temperature_change',
    'old_value': 21.5,
    'new_value': 22.0,
    'trigger': 'schedule'
}
```

## Best Practices

1. **Memory Management**
   ```python
   # For large datasets, use generators
   def log_generator(module, count):
       for _ in range(count):
           yield module.generate_log()
   ```

2. **Error Handling**
   ```python
   from contextlib import contextmanager

   @contextmanager
   def safe_log_generation():
       try:
           yield
       except Exception as e:
           print(f"Error generating log: {e}")
           yield None
   ```

3. **Parallel Processing**
   ```python
   from concurrent.futures import ThreadPoolExecutor

   def parallel_generate(modules, count_per_module):
       with ThreadPoolExecutor() as executor:
           futures = [
               executor.submit(generate_batch, module, count_per_module)
               for module in modules
           ]
           return [f.result() for f in futures]
   ```

## Integration Testing

```python
def test_log_generation():
    """Test log generation for AI model integration."""
    # Generate a small test set
    test_logs = generate_batch(api, 10)

    # Verify log structure
    for log in test_logs:
        assert isinstance(log, dict)
        assert 'timestamp' in log
        assert 'method' in log

    # Test format consistency
    formats = set(str(type(log['status'])) for log in test_logs)
    assert len(formats) == 1  # All status codes should be same type
```

## Performance Tips

When integrating LG3K into your application, consider these optimization tips:

1. Use `generate_batch()` for multiple logs instead of individual calls - this reduces overhead
2. Implement caching in your application for frequently used log patterns
3. Use ThreadPoolExecutor in your code for parallel generation when needed
4. Consider using `ujson` in your application for faster JSON serialization of the generated logs

> 💡 **Contributing to LG3K**: We welcome contributions that improve LG3K's performance! If you have ideas for optimizations or have identified bottlenecks, please feel free to open an issue or submit a pull request.

## Common Use Cases

1. **Training Data Generation**
   - Security anomaly detection
   - Log pattern recognition
   - System behavior analysis

2. **Testing and Validation**
   - Log ingestion systems
   - SIEM integration
   - Monitoring tool development

3. **Documentation and Examples**
   - API documentation
   - Integration guides
   - Training materials
