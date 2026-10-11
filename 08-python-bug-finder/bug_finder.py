"""Find common Python bugs and bad practices by reading the code's syntax tree."""
import ast


def find_issues(source):
    """Return a sorted list of (line_number, message) tuples."""
    tree = ast.parse(source)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = list(node.args.defaults) + [d for d in node.args.kw_defaults if d is not None]
            for default in defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append((node.lineno, f"mutable default argument in '{node.name}'"))

        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append((node.lineno, "bare 'except:' also catches KeyboardInterrupt and SystemExit"))

        elif isinstance(node, ast.Compare):
            for op, right in zip(node.ops, node.comparators):
                if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(right, ast.Constant) and right.value is None:
                    issues.append((node.lineno, "compare to None with 'is' or 'is not', not '==' or '!='"))

        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
            issues.append((node.lineno, "eval() runs arbitrary code if the input is not trusted"))

    return sorted(issues)
