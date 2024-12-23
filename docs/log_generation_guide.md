# Log Generation Guide for LG3K

This guide explains how to generate various types of logs using LG3K, including configuration options and output formats.

## Overview

LG3K is a flexible log generator that supports multiple log types, output formats, and configuration options. This guide covers all aspects of log generation.

## Quick Start

```bash
# Generate basic logs
lg3k --count 1000 --threads 4

# Generate logs with specific services
lg3k --count 1000 --services web_server,database,api

# Generate logs in simple mode (no rich output)
lg3k --count 1000 --simple

# Generate logs in JSON format
lg3k --count 1000 --json-output
```

## Configuration

### Generate Default Config
```bash
lg3k --generate-config config.json
```

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
    "threads": 4,
    "simple": false,
    "llm_format": false,
    "keep_files": false
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
- Description: Number of log entries per service
- Default: 100
- Maximum: 1,000,000

#### threads
- Type: Integer
- Description: Number of threads for parallel generation
- Default: System CPU count
- Minimum: 1

#### simple
- Type: Boolean
- Description: Use simple output mode
- Default: false

#### llm_format
- Type: Boolean
- Description: Generate LLM training format
- Default: false

#### keep_files
- Type: Boolean
- Description: Keep generated files
- Default: false

## Output Formats

### Standard Output
```text
[Thread 1] ██████▉ 90% (90/100 logs)
[Thread 2] █████████▌ 100% (100/100 logs) Completed: logs_part2.json
```

### Simple Output
```text
Starting log generation for 1000 logs across 10 files.
Thread 1 completed generating ./logs/logs_part1.json
Thread 2 completed generating ./logs/logs_part2.json
```

### JSON Output
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
    }
}
```

## Log Types and Examples

### Web Server Logs
```json
{
    "timestamp": "2024-03-22T15:30:45Z",
    "method": "GET",
    "path": "/api/v1/users",
    "status": 200,
    "response_time": 45,
    "client_ip": "192.168.1.100"
}
```

### Database Logs
```json
{
    "timestamp": "2024-03-22T15:30:45Z",
    "operation": "SELECT",
    "table": "users",
    "duration": 150,
    "rows_affected": 10,
    "query_id": "q123456"
}
```

### API Logs
```json
{
    "timestamp": "2024-03-22T15:30:45Z",
    "endpoint": "/v1/users",
    "method": "POST",
    "status": 201,
    "response_time": 120,
    "client_id": "api_client_123"
}
```

## Command Line Options

```bash
# Basic log generation
lg3k --count 1000 --threads 4

# Specific services
lg3k --services web_server,database,api

# Output directory
lg3k --output-dir ./logs

# JSON output
lg3k --json-output

# Simple mode (no rich output)
lg3k --simple

# Keep generated files
lg3k --keep-files

# Generate config
lg3k --generate-config config.json
```

## Progress Tracking

### Docker-Style Progress
```text
1ff5d2e3: web_server   [=========>  ] 50.0%
5520ebfb: database     [==========] Complete
e9c8c5d6: api         [>         ] Waiting
```

### Status Updates
- Running: Active log generation
- Complete: Finished successfully
- Error: Generation failed
- Cancelled: User interrupted
- Waiting: In queue

## File Management

### Output Directory Structure
```
logs/
├── web_server_logs.json
├── database_logs.json
├── api_logs.json
└── combined_logs.json
```

### File Cleanup
- Automatic cleanup on error (unless --keep-files)
- Manual cleanup with CTRL+C
- Keep files with --keep-files flag

## Best Practices

1. **Performance**
   - Use appropriate thread count
   - Monitor system resources
   - Balance log count per service

2. **File Management**
   - Use meaningful output directories
   - Enable keep_files for important data
   - Clean up temporary files

3. **Configuration**
   - Use config files for repeatability
   - Override with command line when needed
   - Document custom configurations

4. **Error Handling**
   - Monitor progress output
   - Check error messages
   - Use appropriate cleanup options

## Troubleshooting

Common issues and solutions:
- Permission errors: Check output directory permissions
- Memory usage: Reduce thread count or batch size
- Slow generation: Adjust thread count
- File conflicts: Use unique output directories

## Next Steps

1. Start with small log counts to test
2. Experiment with different services
3. Try various output formats
4. Create custom configurations
5. Automate log generation

For more advanced usage, see:
- [Developer Guide](developer_guide.md) for programmatic usage
- [Llama Training How-To](llama_training_howto.md) for LLM training
