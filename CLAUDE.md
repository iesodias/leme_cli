# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python CLI tool for generating, managing, and executing Infrastructure as Code (IaC) projects with Terraform. It supports AWS and Azure providers and uses Jinja2 templates to generate Terraform configurations.

## Dependencies

The CLI requires the following Python packages (install manually as needed):
- `typer` - CLI framework
- `rich` - Terminal formatting
- `jinja2` - Template engine

Install dependencies: `pip install typer rich jinja2`

## Code Structure

The project has been modularized for better maintainability:

- `src/` - Source code modules
  - `commands/` - CLI command implementations
  - `config/` - Configuration, constants, and validation
  - `templates/` - Template management
  - `terraform/` - Terraform execution utilities
  - `system/` - System detection and tool installation

## Running the CLI

Main entry point: `python3 main.py`

The CLI requires dependencies to be installed first. The tool will show an error if dependencies are missing.

## Commands

### Creating Projects and Resources

- `python3 main.py new project --name <project_name> --provider <aws|azure>` - Creates a new Terraform project
- `python3 main.py new module --name <module_name>` - Creates a reusable Terraform module
- `python3 main.py new resource --type <resource_type> --provider <aws|azure> --name <resource_name>` - Creates a resource module

### Managing Projects

- `python3 main.py delete <project_path>` - Deletes a project directory (with confirmation)
- `python3 main.py delete <project_path> --force` - Force delete without confirmation

### Running Terraform

- `python3 main.py run <init|validate|plan|apply|destroy> <project_path>` - Executes Terraform commands

Requires Terraform to be installed and available in PATH.

### Installing Tools

- `python3 main.py install docker` - Installs Docker automatically based on OS
- `python3 main.py install docker --check-only` - Check if Docker is installed
- `python3 main.py install docker --manual` - Show manual installation instructions
- `python3 main.py install docker --force` - Force reinstallation
- `python3 main.py status` - Check status of installed tools
- `python3 main.py system-info` - Show detailed system information
- `python3 main.py uninstall-docker` - Remove Docker from system

### System Information

- `python3 main.py system-info` - Shows OS, architecture, WSL status, package manager
- `python3 main.py status` - Shows Docker installation and working status

## Architecture

### Core Structure

- `main.py` - Main CLI application using Typer framework
- `templates/` - Jinja2 templates for generating Terraform code
  - `providers/aws/` - AWS-specific templates
  - `providers/azure/` - Azure-specific templates  
  - `common/` - Shared templates (gitignore, etc.)

### Template System

The tool uses Jinja2 templates to generate Terraform configurations:

- Project templates: Complete project structure with backend, providers, main.tf
- Resource templates: Individual resource modules (storage accounts, VMs, etc.)
- Provider-specific templates for AWS and Azure

### Key Patterns

1. **Modular Architecture**: Code is organized into separate modules for commands, validation, templates, and Terraform execution
2. **Validation Layer**: Comprehensive input validation and error handling with custom exceptions
3. **Template Management**: Centralized template rendering with validation and error handling
4. **Provider Abstraction**: Same CLI commands work for both AWS and Azure with different templates
5. **Constants and Configuration**: Centralized configuration management in `src/config/constants.py`

### Resource Types

Currently supported Azure resources:
- `storage-account` - Azure Storage Account with resource group
- `virtual_machine` - Azure Virtual Machine

AWS support exists but templates may be incomplete.

### Example Generated Structure

```
project-name/
├── main.tf
├── variables.tf  
├── outputs.tf
├── providers.tf
├── backend.tf
└── .gitignore
```