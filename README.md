<h1><p align="center">
  <img src="./docs/_image/logo-large.svg" alt="DeepH-dock Logo" width="500">
</p></h1>

<div align="center">

###  A Universal Interface for Quantum Materials Calculations

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![GitHub Issues](https://img.shields.io/github/issues/kYangLi/DeepH-dock.svg)](https://github.com/kYangLi/DeepH-dock/issues)
[![GitHub Stars](https://img.shields.io/github/stars/kYangLi/DeepH-dock.svg?style=social)](https://github.com/kYangLi/DeepH-dock/stargazers)

*Modular, extensible bridge between first-principles calculations and DeepH method*
</div>

`DeepH-dock` is a **modular, extensible interface platform for quantum materials calculations, dedicated to building efficient and reliable bridges between first-principles calculations and the DeepH (deep learning Hamiltonian) method.** This platform integrates multiple density functional theory (DFT) software interfaces, supports DeepH predictions, and provides standardized data processing.

At the core of DeepH-dock is **a unified and flexible interface layer that seamlessly connects mainstream DFT packages with the DeepH workflow**, enabling users to generate and utilize deep learning-based Hamiltonians with minimal effort. DeepH-dock offers first-class support for heterogeneous computational environments, allowing researchers to orchestrate complex multi-software workflows through a consistent Python API. Designed to significantly lower the technical barrier and enhance reproducibility in large-scale quantum materials simulations, `DeepH-dock` is the product of extensive refinement driven by real-world research needs.

## Core Features

### 🧬 Multi-Software Compatibility

- **DFT Software Support**: OpenMX, VASP, Quantum ESPRESSO, FHI-aims, SIESTA, PySCF, ABACUS, etc.
- **Deep Learning Frameworks**: Neural network model interfaces including DeepH, DeepH-E3, DeepH-2, etc.
- **Tight-Binding Toolchain**: WannierTools, HopTB, HopCP, Z2Pack, etc.

### ⚡ High-Performance Computational Core

- **Fast Diagonalization Algorithms**: Implementation of efficient numerical methods such as KPM and Lanczos
- **Structure Generation Algorithms**: Automatic generation of crystal/molecular configurations
- **Hamiltonian Processing**: Symmetrization, error evaluation, and other general operations
- **Overlap Matrix Processing**: Calculation of overlap matrix under given basis and atomic structures

### 🔄 Standardized Workflows

- **Data Generation**: Automated DFT computational data generation pipelines
- **Preprocessing**: Standardized feature extraction and data cleaning
- **Postprocessing**: Result analysis and visualization tools
- **Composite Workflows**: Support for custom computational pipelines

### 🛠️ Utility Toolkit

- **Parallel Computing**: Multi-level parallel support including MPI and Loky
- **Format Conversion**: Various data format conversion tools (.h5, .petsc, .csc, etc.)
- **Validation Tools**: Data integrity and consistency verification

## Quick Start

### Installation

```bash
git clone https://github.com/kYangLi/DeepH-dock.git
cd DeepH-dock
pip install -e .
```

### Basic Usage

run `dock -h`,

```bash
Usage: dock [OPTIONS] COMMAND [ARGS]...

  DeepH-dock: Materials Computation and Data Analysis Toolkit.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  analyze
  compute
  convert
  design
  ls       List all available commands.
```

## Project Architecture

DeepH-dock is structured as a modular system with clearly defined functional responsibilities:

- **Analysis Module** (`analyze/`): Data analysis, visualization, and post-processing utilities
- **Computation Module** (`compute/`): Core physical quantity calculations and algorithmic implementations
- **Conversion Module** (`convert/`): Data format transformations and interoperability between different software packages
- **Design Module** (`design/`): Material structure generation, manipulation, and design workflows
- **HPRO Integration** (`hpro/`): Specialized interfaces and utilities for a modified [`HPRO`](https://github.com/Xiaoxun-Gong/HPRO) library operations

This modular design ensures clear separation of concerns while maintaining interoperability between components, enabling flexible and scalable computational workflows.

## Application Scenarios

- **High-Throughput Materials Calculations**: Automated generation and processing of electronic structure data for large material sets
- **Deep Learning Training Data Preparation**: Preparing standardized training datasets for neural network models
- **Tight-Binding Parameter Fitting**: Connecting DFT calculations with tight-binding model parameterization
- **Method Development and Validation**: Rapid implementation and testing of new computational algorithms

## Contributing

We welcome contributions from the community! To ensure a consistent and maintainable codebase, please follow the structured workflow below when adding new functionality.

### Development Workflow for Contributors

1. **Identify the Target Module**

    First, determine which major module your contribution belongs to, based on the project architecture (e.g., `analyze`, `compute`, `convert`, `design`).

2. **Create Your Submodule**

    Create a new folder for your submodule within the corresponding parent module. For example, if you are implementing an interface between FHI-aims and DeepH, create it under `deepx_dock/convert/fhi_aims/`.

3. **Implement Your Functionality**

    Package the core logic you wish to add as a well-defined Python class or function. This makes the code reusable and easier to test.

4. **Register a Command-Line Interface (CLI)**

    **This is the most important step.** To expose your functionality through the main `dock` command, you must register your function inside the `_cli.py` file within your submodule directory.

    In this file, define your CLI command using the `click` library and the provided `@register` decorator.

**Example:**
If you create `deepx_dock/convert/fhi_aims/_cli.py` with the following content:

```python
import click
from pathlib import Path
from deepx_dock._cli.registry import register

@register(
    cli_name="my-func",
    cli_help="A brief description of what my-func does.",
    cli_args=[
        click.argument('fhiaims_dir', type=click.Path()),
        click.argument('deeph_dir', type=click.Path()),
        click.option(
            '--parallel-num', '-p', type=int, default=-1,
            help="The parallel processing number, -1 for using all of the cores."
        ),
    ],
)
def my_func(fhiaims_dir: Path, deeph_dir: Path, parallel_num: int):
    # Your implementation logic here
    from .my_wanderful_function import my_real_func
    my_real_func(fhiaims_dir, deeph_dir, parallel_num)
```

Then, on the user end, a new command will be available:

```bash
dock convert fhi-aims my-func
```

The command's usage (arguments, options, help text) is entirely defined by the `click` decorators specified in `cli_args`. Please refer to the [official click documentation](https://click.palletsprojects.com/) for details on defining arguments and options.

For additional details, refer to the [Development Guide](https://deeph-dock.readthedocs.io/en/latest/for_developers/development_guide.html).

## Citation

If you use this platform, please cite:

```bash
TBA
```

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.

## Support & Contact

- 📖 **Documentation**: [Documentation Link](https://deeph-dock.readthedocs.io)
- 🐛 **Issue Reporting**: [GitHub Issues](https://github.com/kYangLi/DeepH-dock/issues)
<!-- - 💬 **Discussions**: [GitHub Discussions]() -->

---

*DeepH-dock is community-driven development for quantum materials calculations, aiming to promote openness and reproducibility in computational materials science research.*
