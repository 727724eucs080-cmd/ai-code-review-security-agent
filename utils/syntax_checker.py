"""
syntax_checker.py

Checks syntax of Python and Java source code.
"""
import ast
import subprocess
import tempfile
import os

# -----------------------------
# Python Syntax Checker
# -----------------------------

def check_python_syntax(source_code):

    try:

        ast.parse(source_code)

        return {
            "language": "Python",
            "status": "Valid",
            "message": "Python syntax is correct."
        }

    except SyntaxError as error:

        return {
            "language": "Python",
            "status": "Invalid",
            "message": (
                f"Line {error.lineno}: {error.msg}"
            )
        }

    except Exception as error:

        return {
            "language": "Python",
            "status": "Error",
            "message": str(error)
        }

# -----------------------------
# Java Syntax Checker
# -----------------------------

def check_java_syntax(source_code):

    try:

        # Create temporary Java file

        with tempfile.TemporaryDirectory() as temp_dir:

            java_file = os.path.join(
                temp_dir,
                "Main.java"
            )

            with open(
                java_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(source_code)

            # Run Java compiler

            result = subprocess.run(

                [
                    "javac",
                    java_file
                ],

                capture_output=True,

                text=True
            )

            if result.returncode == 0:

                return {

                    "language": "Java",

                    "status": "Valid",

                    "message": "Java syntax is correct."

                }

            else:
                return {

                    "language": "Java",

                    "status": "Invalid",

                    "message": result.stderr
                }

    except FileNotFoundError:

        return {

            "language": "Java",

            "status": "Error",

            "message":
            "Java compiler not found. Install JDK and configure PATH."
        }
    except Exception as error:
        
        return {

            "language": "Java",

            "status": "Error",

            "message": str(error)
        }