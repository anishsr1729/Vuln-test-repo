
import os
import sqlite3
import subprocess
import pickle
import hashlib
from pathlib import Path


# ============================================================
# Deliberately Vulnerable Test Application
# FOR SECURITY AGENT TESTING ONLY
#
# This application intentionally contains security weaknesses.
# Do not deploy it or expose it to untrusted users.
# Vulnerable functions are not executed automatically.
# ============================================================


# VULNERABILITY 1: Hardcoded credential
DATABASE_PASSWORD = "admin123"
API_SECRET = "super-secret-hardcoded-key"


# ------------------------------------------------------------
# VULNERABILITY 2: Unsafe dynamic expression evaluation
# Expected scanner: Bandit B307
# ------------------------------------------------------------
def calculate_expression(expression):
    """Calculate a mathematical expression."""
    return eval(expression)


# ------------------------------------------------------------
# VULNERABILITY 3: Shell command injection
# Expected scanner: Bandit B602
# ------------------------------------------------------------
def generate_report(user_input):
    """Generate a report using a shell command."""
    command = f"echo Generating report for {user_input}"

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout


# ------------------------------------------------------------
# VULNERABILITY 4: SQL injection
# ------------------------------------------------------------
def get_user(username):
    """Retrieve a user from the database."""
    connection = sqlite3.connect("application.db")
    cursor = connection.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"

    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()
    return result


# ------------------------------------------------------------
# VULNERABILITY 5: Unsafe deserialization
# Expected scanner: Bandit B301
# ------------------------------------------------------------
def load_user_data(serialized_data):
    """Load serialized user information."""
    return pickle.loads(serialized_data)


# ------------------------------------------------------------
# VULNERABILITY 6: Path traversal
# ------------------------------------------------------------
def read_user_file(filename):
    """Read a file requested by the user."""
    base_directory = os.path.join(os.getcwd(), "user_files")
    file_path = os.path.join(base_directory, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# ------------------------------------------------------------
# VULNERABILITY 7: Weak cryptographic hash
# Expected scanner: Bandit B324
# ------------------------------------------------------------
def generate_file_hash(data):
    """Generate a hash for supplied data."""
    return hashlib.md5(data.encode()).hexdigest()


# ------------------------------------------------------------
# VULNERABILITY 8: Weak password verification
# ------------------------------------------------------------
def verify_password(input_password):
    """Verify an application password."""
    if input_password == DATABASE_PASSWORD:
        return True

    return False


# ------------------------------------------------------------
# VULNERABILITY 9: Missing network timeout
# ------------------------------------------------------------
def fetch_remote_data(url):
    """Fetch data from a remote URL."""
    import urllib.request

    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


# ------------------------------------------------------------
# Application entry point
# ------------------------------------------------------------
def main():
    print("Vulnerable Test Application")
    print("This application is intended for security testing.")
    print("Vulnerable functions are not executed automatically.")


if __name__ == "__main__":
    main()
