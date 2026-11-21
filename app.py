
import ast
import operator
import ipaddress
import os
import re
import shutil
import subprocess
import sqlite3


def calculate_expression(expression):
    if len(expression) > 1000:
        raise ValueError("expression is too large")
    tree = ast.parse(expression, mode="eval")

    def evaluate(node, depth=0):
        if depth > 100:
            raise ValueError("expression nesting is too deep")
        if isinstance(node, ast.Expression):
            return evaluate(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 10 ** 100:
                raise ValueError("numeric result is too large")
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand, depth + 1)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            operations = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Mod: operator.mod,
                ast.Pow: operator.pow,
            }
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("unsupported arithmetic operator")
            left = evaluate(node.left, depth + 1)
            right = evaluate(node.right, depth + 1)
            if isinstance(node.op, ast.Pow) and (abs(right) > 1000 or abs(left) > 10 ** 50):
                raise ValueError("exponentiation is too large")
            result = operation(left, right)
            if abs(result) > 10 ** 100:
                raise ValueError("numeric result is too large")
            return result
        raise ValueError("only basic arithmetic expressions are allowed")

    return evaluate(tree)


def get_user_info(username):
    # Vulnerability: SQL injection through string concatenation
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    result = cursor.fetchall()
    connection.close()

    return result


def ping_host(host):
    if not isinstance(host, str) or not host or host.startswith("-"):
        raise ValueError("invalid host")
    if any(character.isspace() for character in host):
        raise ValueError("invalid host")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?", host):
            raise ValueError("invalid host")
    executable = shutil.which("ping")
    if executable is None:
        raise FileNotFoundError("ping executable not found")
    return subprocess.run([executable, "-c", "1", host], shell=False, check=False).returncode


def read_file(filename):
    # Vulnerability: Potential path traversal
    with open(filename, "r") as file:
        return file.read()


if __name__ == "__main__":
    print("Vulnerable application started")
