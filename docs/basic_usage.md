# Basic Usage

DeepH-dock offers flexible usage through both a command-line interface (CLI) and a Python API, catering to different user workflows and integration needs.

## 1. Command-line Interface (CLI)

The primary entry point for DeepH-dock is the `dock` command, providing access to all functionalities through a modular, hierarchical interface.

### Exploring the Command Structure

To see the available top-level modules and commands, use:

```bash
dock -h
```

This displays the main structure of DeepH-dock:

```bash
Usage: dock [OPTIONS] COMMAND [ARGS]...

DeepH-dock: Materials Computation and Data Analysis Toolkit.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  analyze     Data analysis and processing tools
  compute     DFT calculation drivers and workflows
  convert     Data format converters between DFT codes
  design      Structure generation and manipulation
  ls          List all available commands
```

### Navigating Command Hierarchy

Each module contains specific subcommands organized in a tree structure. You can explore this hierarchy layer by layer:

```bash
# View commands in the analyze module
dock analyze -h

# View subcommands in the error analysis section
dock analyze error -h

# Get detailed help for a specific command
dock analyze error element -h
```

This hierarchical approach allows you to discover functionality progressively, from general categories to specific tools.

### Discovering All Available Commands

If you prefer to see all available commands at once, use:

```bash
dock ls
```

This provides a comprehensive list of all registered commands, organized by module:

```bash
✨ Available Commands ✨
Total: 32 commands
────────────────────────────────────────────────────────────────────────────────

📦 analyze.dataset
───────────────────
dock analyze dataset edge
  Statistic and show edge related information.

dock analyze dataset split
  Generate train, validate, and test data split json file.

...

📦 design.twist-2d
───────────────────
dock design twist-2d stack
  Generate twisted 2D heterostructures with custom parameters.


💡 Usage Examples:
  dock module command [options]
  dock --help - Show general help
  dock module --help - Show help for a module
  dock module command --help - Show help for a command
────────────────────────────────────────────────────────────────────────────────
```

### Common Workflow Examples

Here are practical examples demonstrating typical usage patterns:

```bash
# Convert OpenMX output to DeepH format
dock convert openmx to-deeph ./openmx_data ./deeph_data
```

```bash
# Create a twisted bilayer structure
dock design twist-2d stack "POSCAR-C" "7,8,-8,15" "POSCAR-BN" "8,7,-7,15"
```

## 2. Python API

For programmatic access and integration into custom workflows, DeepH-dock provides a comprehensive Python API.

### Direct Module Import

You can import and use any module directly in your Python scripts:

```python
from deepx_dock.design.twist_2d.twist import Twist2D

# Initialize and create a twisted bilayer structure
twist_2d = Twist2D()
m, n = 7, 8

# Add individual layers
twist_2d.add_layer([m, n], [-n, m+n], prim_poscar="./POSCAR-C")
twist_2d.add_layer([n, m], [-m, n+m], prim_poscar="./POSCAR-BN")

# Apply twist between layers
twist_2d.twist_layers()

# Export the resulting structure
twist_2d.write_res_to_poscar("twisted_bilayer.vasp")
```

### Building Workflows Like LEGO® Bricks

DeepH-dock is built with a modular architecture, allowing you to easily combine different functions brick by brick to construct complex and customized workflows.

```python
# Convert data using the convert module
from deepx_dock.convert.openmx.translate_openmx_to_deeph import OpenMXDatasetTranslator

translator = OpenMXDatasetTranslator("./openmx_data", "./deeph_data")
translator.transfer_all_openmx_to_deeph()

# Analyze data using the analyze module
from deepx_dock.analyze.error.with_infer_res import ErrorElementsPairDistributionAnalyzer

dist = ErrorElementsPairDistributionAnalyzer("./deeph_data", pred_only=True)
dist.analyze_all()
dist.plot()
```

## 3. Learning Through Examples

The best way to learn DeepH-dock is through practical examples. Visit the [`examples/`](https://github.com/kYangLi/DeepH-dock/tree/main/examples) directory or the [Capabilities](./capabilities/index.rst) in the repository for Jupyter notebooks demonstrating various use cases:

- **Basic workflows** - Getting started with common tasks
- **Advanced analyses** - Complex data processing and visualization
- **Integration patterns** - Combining DeepH-dock with other tools

## 4. Extending DeepH-dock

DeepH-dock is designed with extensibility in mind. If you want to add new functionality:

1. **Use existing modules** as building blocks for custom workflows
2. **Extend functionality** by adding new methods to existing classes
3. **Create new modules** following the project's modular architecture

For detailed instructions on extending DeepH-dock, creating new CLI commands, and contributing to the project, please refer to the [Development Guide](./for_developers/development_guide.md).

The framework makes it straightforward to add new functionality that automatically integrates with the command-line interface, requiring only minimal boilerplate code once your core Python functions are implemented.

## Need Help?

- Use `dock [module] --help` for command-specific assistance
- Check the [`examples/`](https://github.com/kYangLi/DeepH-dock/tree/main/examples) directory for practical implementations
- For development questions, see the [For Developers](./for_developers/index.rst) section
- Browse the [Capabilities](./capabilities/index.rst) section for an overview of all available functionality
