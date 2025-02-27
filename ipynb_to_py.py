import nbformat
import argparse
import logging
import re
import ast
import astunparse
import subprocess
import tempfile
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_ipynb_to_py(ipynb_path, py_path, remove_unused=True, use_black=True):
    """
    Converts an IPython Notebook (.ipynb) to a Python script (.py).

    Args:
        ipynb_path (str): Path to the input .ipynb file.
        py_path (str): Path to the output .py file.
        remove_unused (bool): Whether to remove unused variables.
        use_black (bool): Whether to use black for formatting.
    """
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        python_code = ""
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                source_code = cell.source
                if remove_unused:
                    source_code = remove_unused_variables(source_code)
                python_code += source_code + "\n\n"
            elif cell.cell_type == 'markdown':
                markdown_lines = cell.source.splitlines()
                commented_markdown = "\n# " + "\n# ".join(markdown_lines) + "\n\n"
                python_code += commented_markdown

        # Format the generated Python code
        if use_black:
            formatted_code, changes = format_with_black(python_code)
            if changes:
                logging.info(f"Formatting changes applied to: {ipynb_path} (using black)")
                for change in changes:
                    logging.info(f"  - {change}")
        else:
            formatted_code, changes = format_code(python_code)
            if changes:
                logging.info(f"Formatting changes applied to: {ipynb_path}")
                for change in changes:
                    logging.info(f"  - {change}")

        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(formatted_code)

        logging.info(f"Successfully converted {ipynb_path} to {py_path}")

    except FileNotFoundError:
        logging.error(f"File not found: {ipynb_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def remove_unused_variables(source_code):
    """
    Removes unused variables from the given Python source code.

    Args:
        source_code (str): Python source code.

    Returns:
        str: Python source code with unused variables removed.
    """
    try:
        tree = ast.parse(source_code)
        used_vars = set()
        defined_vars = set()

        # Find all used variables
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)

        # Find all defined variables
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_vars.add(target.id)

            elif isinstance(node, ast.For):
                if isinstance(node.target, ast.Name):
                    defined_vars.add(node.target.id)

            elif isinstance(node, ast.FunctionDef):
                defined_vars.add(node.name)
                for arg in node.args.args:
                    defined_vars.add(arg.arg)

            elif isinstance(node, ast.ClassDef):
                defined_vars.add(node.name)

        unused_vars = defined_vars - used_vars

        # Remove assignments of unused variables
        new_tree = ast.Module(body=[])
        for node in tree.body:
            if isinstance(node, ast.Assign):
                targets = []
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id not in unused_vars:
                        targets.append(target)
                if targets:
                    new_node = ast.Assign(targets=targets, value=node.value, type_comment=node.type_comment)
                    new_tree.body.append(new_node)
            elif isinstance(node, ast.FunctionDef):
                new_tree.body.append(node)
            elif isinstance(node, ast.ClassDef):
                new_tree.body.append(node)
            else:
                new_tree.body.append(node)

        return astunparse.unparse(new_tree)

    except SyntaxError as e:
        logging.warning(f"Syntax error, skipping variable removal: {e}")
        return source_code

def format_code(source_code):
    """
    Formats Python code using a basic approach (adding newlines around function and class definitions).

    Args:
        source_code (str): Python source code.

    Returns:
        tuple: Formatted code and a list of changes made.
    """
    lines = source_code.splitlines()
    formatted_lines = []
    changes = []
    prev_line_empty = True

    for i, line in enumerate(lines):
        if line.startswith("def ") or line.startswith("class "):
            if not prev_line_empty and formatted_lines:
                formatted_lines.append("")
                changes.append(f"Added newline before function/class definition at line {i+1}")
            formatted_lines.append(line)
            formatted_lines.append("")
            prev_line_empty = True
        else:
            formatted_lines.append(line)
            prev_line_empty = not line.strip()

    return "\n".join(formatted_lines), changes

def format_with_black(source_code):
    """
    Formats Python code using black.

    Args:
        source_code (str): Python source code.

    Returns:
        tuple: Formatted code and a list of changes made.
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
            temp_file.write(source_code)
            temp_file_path = temp_file.name

        subprocess.run(['black', temp_file_path], check=True, capture_output=True)

        with open(temp_file_path, 'r', encoding='utf-8') as formatted_file:
            formatted_code = formatted_file.read()

        os.unlink(temp_file_path) #delete temp file.
        return formatted_code, ["Formatted using black"]

    except FileNotFoundError:
        logging.warning("black not found. Using basic formatter.")
        return format_code(source_code)
    except subprocess.CalledProcessError as e:
        logging.warning(f"black formatting failed: {e}")
        return source_code, [f"black formatting failed: {e}"]
    except Exception as e:
        logging.warning(f"black formatting error: {e}")
        return source_code, [f"black formatting error: {e}"]

def main():
    """
    CLI interface for the script.
    """
    parser = argparse.ArgumentParser(description="Convert .ipynb to .py")
    parser.add_argument("input_ipynb", help="Path to the input .ipynb file")
    parser.add_argument("output_py", help="Path to the output .py file")
    parser.add_argument("--no-remove-unused", action="store_false", dest="remove_unused", help="Disable removal of unused variables")
    parser.add_argument("--no-black", action="store_false", dest="use_black", help="Disable black formatting")
    args = parser.parse_args()

    convert_ipynb_to_py(args.input_ipynb, args.output_py, args.remove_unused, args.use_black)

if __name__ == "__main__":
    main()