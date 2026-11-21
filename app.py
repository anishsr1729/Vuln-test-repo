
import os
import subprocess
import sqlite3


def calculate_expression(expression):
    # Vulnerability: Arbitrary code execution through eval()
    return eval(expression)


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
    # Vulnerability: Shell command injection
    command = "ping -c 1 " + host
    return subprocess.call(command, shell=True)


def read_file(filename):
    # Vulnerability: Potential path traversal
    with open(filename, "r") as file:
        return file.read()


if __name__ == "__main__":
    print("Vulnerable application started")
