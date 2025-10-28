# MacbookAir

Personal scripts and utilities repository for automation, system administration, and learning purposes.

## Overview

This repository contains a collection of shell scripts, Python programs, and Kubernetes configurations used for various automation tasks and practice exercises.

## Directory Structure

```
.
├── shell/          # Bash scripts for system automation
├── python/         # Python scripts and programs
├── k8s/yaml/       # Kubernetes pod definitions
└── docker/         # Docker-related files
```

## Contents

### Shell Scripts

- **clear_log.sh** - Automated log cleanup script
  - Runs monthly on the last day of each month
  - Cleans log files older than 30 days from `/tmp/dumas/`
  - Comprehensive logging to `/var/log/log_cleanup.log`

- **vim_practice.sh** - Vim editor practice script

### Python Programs

- **hello_response.py** - Interactive Python program with robust input handling

### Kubernetes

- **initPod.yml** - Kubernetes pod configuration file

## Usage

### Running Shell Scripts

```bash
bash shell/clear_log.sh
bash shell/vim_practice.sh
```

### Running Python Scripts

```bash
python3 python/hello_response.py
```

### Installing Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Applying Kubernetes Configurations

```bash
kubectl apply -f k8s/yaml/initPod.yml
```

## Features

- **Comprehensive Documentation**: All scripts include detailed inline comments
- **Error Handling**: Robust error checking and logging
- **Best Practices**: Follows shell scripting and Python coding standards
- **Educational**: Well-documented for learning purposes

## Requirements

- Bash shell
- Python 3.7+
- kubectl (for Kubernetes configurations)

## License

MIT License - See LICENSE file for details
