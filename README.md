# ipynb-to-py

A Python script to convert Jupyter Notebook (`.ipynb`) files to Python (`.py`) scripts, with features for removing unused variables, code formatting (using `black`), and markdown cell commenting.

## Features

* **Markdown to Comments:** Converts markdown cells into Python comments.
* **Code Formatting:** Formats Python code using `black` (if available) or a basic formatter.
* **Unused Variable Removal:** Removes unused variables from code cells using static analysis.
* **CLI Interface:** Easy-to-use command-line interface.
* **Logging:** Provides detailed logging of the conversion process.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd ipynb-to-py
    ```

2.  **Create a Conda environment (recommended):**

    ```bash
    conda create -n ipynb_converter python=3.9 # or your preferred python version
    conda activate ipynb_converter
    ```

3.  **Install dependencies:**

    ```bash
    conda install nbformat astunparse black #or pip install nbformat astunparse black
    ```

## Usage

```bash
python ipynb_to_py.py <input.ipynb> <output.py> [flags]
```

Flags

    input.ipynb: Path to the input Jupyter Notebook file.
    output.py: Path to the output Python script.
    --no-remove-unused: Disables the removal of unused variables.
    --no-black: Disables black formatting.
