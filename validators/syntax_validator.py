import ast
import os
import re
import subprocess
import tempfile


class SyntaxValidator:
    """
    Validates Python and Java source code before
    sending it to the analysis workflow.
    """

    @staticmethod
    def validate_python(code: str):
        try:
            ast.parse(code)

            return {
                "valid": True,
                "message": "Python syntax is valid.",
                "line": None,
                "column": None,
                "error": None,
                "source_line": None,
                "pointer": "",
            }

        except SyntaxError as error:
            line_number = error.lineno
            column_number = error.offset
            error_message = error.msg or "Invalid Python syntax."

            source_line = ""

            if error.text:
                source_line = error.text.rstrip("\n")

            pointer = ""

            if column_number is not None and column_number > 0:
                pointer = " " * (column_number - 1) + "^"

            formatted_message = (
                f"Syntax error at line {line_number}, "
                f"column {column_number}: "
                f"{error_message}"
            )

            return {
                "valid": False,
                "message": formatted_message,
                "line": line_number,
                "column": column_number,
                "error": error_message,
                "source_line": source_line,
                "pointer": pointer,
            }

        except (ValueError, TypeError, MemoryError, RecursionError) as error:
            return {
                "valid": False,
                "message": f"Unable to parse Python source: {error}",
                "line": None,
                "column": None,
                "error": str(error),
                "source_line": None,
                "pointer": "",
            }

    @staticmethod
    def validate_java(code: str):
        temp_dir = None

        try:
            temp_dir = tempfile.mkdtemp(prefix="java_syntax_")

            public_class_match = re.search(
                r"\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)",
                code
            )

            class_match = re.search(
                r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)",
                code
            )

            if public_class_match:
                class_name = public_class_match.group(1)

            elif class_match:
                class_name = class_match.group(1)

            else:
                class_name = "Temp"

            file_name = f"{class_name}.java"

            file_path = os.path.join(
                temp_dir,
                file_name
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as source_file:

                source_file.write(code)

            result = subprocess.run(
                [
                    "javac",
                    file_path
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "valid": True,
                    "message": "Java syntax is valid.",
                    "line": None,
                    "column": None,
                    "error": None,
                    "source_line": None,
                    "pointer": "",
                }

            error_output = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Java compilation failed."
            )

            line_number = None
            column_number = None
            error_message = error_output
            source_line = ""
            pointer = ""

            match = re.search(
                r":(\d+):\s*(?:error|warning):\s*(.*)",
                error_output
            )

            if match:
                line_number = int(match.group(1))
                error_message = match.group(2).strip()

            source_lines = code.splitlines()

            if (
                line_number is not None
                and 1 <= line_number <= len(source_lines)
            ):
                source_line = source_lines[
                    line_number - 1
                ]

            output_lines = error_output.splitlines()

            for index, output_line in enumerate(output_lines):
                if "^" in output_line:
                    pointer = output_line.strip()
                    break

            formatted_message = error_message

            if line_number is not None:
                formatted_message = (
                    f"Java syntax error at line "
                    f"{line_number}: "
                    f"{error_message}"
                )

            if source_line:
                formatted_message += (
                    f"\n\nLine {line_number}:\n"
                    f"{source_line}"
                )

                if pointer:
                    formatted_message += (
                        f"\n{pointer}"
                    )

            return {
                "valid": False,
                "message": formatted_message,
                "line": line_number,
                "column": column_number,
                "error": error_message,
                "source_line": source_line,
                "pointer": pointer,
            }

        except FileNotFoundError:
            return {
                "valid": False,
                "message": (
                    "Java compiler (javac) not found. "
                    "Please install JDK and add javac to PATH."
                ),
                "line": None,
                "column": None,
                "error": "javac not found",
                "source_line": None,
                "pointer": "",
            }

        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "message": (
                    "Java syntax validation timed out."
                ),
                "line": None,
                "column": None,
                "error": "javac timeout",
                "source_line": None,
                "pointer": "",
            }

        except OSError as error:
            return {
                "valid": False,
                "message": (
                    f"Unable to validate Java source: {error}"
                ),
                "line": None,
                "column": None,
                "error": str(error),
                "source_line": None,
                "pointer": "",
            }

        finally:
            if temp_dir and os.path.exists(temp_dir):
                for root, directories, files in os.walk(
                    temp_dir,
                    topdown=False
                ):
                    for file_name in files:
                        file_path = os.path.join(
                            root,
                            file_name
                        )

                        try:
                            os.remove(file_path)
                        except OSError:
                            pass

                    for directory in directories:
                        directory_path = os.path.join(
                            root,
                            directory
                        )

                        try:
                            os.rmdir(directory_path)
                        except OSError:
                            pass

                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass

    @staticmethod
    def validate(code: str, language: str):
        language = language.lower().strip()

        if not code or not code.strip():
            return {
                "valid": False,
                "message": "Source code cannot be empty.",
                "line": None,
                "column": None,
                "error": "Empty source code",
                "source_line": None,
                "pointer": "",
            }

        if language == "python":
            return SyntaxValidator.validate_python(code)

        if language == "java":
            return SyntaxValidator.validate_java(code)

        return {
            "valid": False,
            "message": (
                f"Unsupported programming language: {language}"
            ),
            "line": None,
            "column": None,
            "error": "Unsupported language",
            "source_line": None,
            "pointer": "",
        }