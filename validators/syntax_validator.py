import ast
import subprocess
import tempfile
import os


class SyntaxValidator:
    """
    Validates Python and Java source code before
    sending it to the AI analysis agents.
    """

    # ==========================================================
    # PYTHON VALIDATION
    # ==========================================================

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
            }

        except SyntaxError as e:

            line_number = e.lineno
            column_number = e.offset
            error_message = e.msg

            source_line = ""

            if e.text:
                source_line = e.text.rstrip("\n")

            pointer = ""

            if column_number is not None and column_number > 0:
                pointer = " " * (column_number - 1) + "^"

            formatted_message = (
                f"Syntax error at line {line_number}, "
                f"column {column_number}: {error_message}"
            )

            if source_line:
                formatted_message += (
                    f"\n\n"
                    f"Line {line_number}:\n"
                    f"{source_line}\n"
                    f"{pointer}"
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

    # ==========================================================
    # JAVA VALIDATION
    # ==========================================================

    @staticmethod
    def validate_java(code: str):

        try:

            with tempfile.TemporaryDirectory() as temp_dir:

                # --------------------------------------------------
                # Find public class name
                # --------------------------------------------------

                import re

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

                # --------------------------------------------------
                # Write Java source
                # --------------------------------------------------

                with open(
                    file_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(code)

                # --------------------------------------------------
                # Run javac
                # --------------------------------------------------

                result = subprocess.run(
                    [
                        "javac",
                        file_path
                    ],
                    capture_output=True,
                    text=True
                )

                # --------------------------------------------------
                # Valid Java
                # --------------------------------------------------

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

                # --------------------------------------------------
                # Invalid Java
                # --------------------------------------------------

                error_output = (
                    result.stderr.strip()
                    or result.stdout.strip()
                )

                line_number = None
                column_number = None
                error_message = error_output
                source_line = ""
                pointer = ""

                # --------------------------------------------------
                # Extract Java compiler line number
                #
                # Example:
                #
                # Temp.java:5: error: ';' expected
                # --------------------------------------------------

                match = re.search(
                    r":(\d+):\s*(?:error|warning):\s*(.*)",
                    error_output
                )

                if match:

                    line_number = int(
                        match.group(1)
                    )

                    error_message = match.group(2).strip()

                # --------------------------------------------------
                # Get source line
                # --------------------------------------------------

                if line_number is not None:

                    source_lines = code.splitlines()

                    if (
                        1 <= line_number
                        <= len(source_lines)
                    ):

                        source_line = (
                            source_lines[
                                line_number - 1
                            ]
                        )

                # --------------------------------------------------
                # Try to extract caret position
                # --------------------------------------------------

                lines = error_output.splitlines()

                for index, line in enumerate(lines):

                    if "^" in line:

                        pointer = line.strip()

                        break

                # --------------------------------------------------
                # Build readable message
                # --------------------------------------------------

                formatted_message = error_message

                if line_number is not None:

                    formatted_message = (
                        f"Java syntax error at "
                        f"line {line_number}: "
                        f"{error_message}"
                    )

                if source_line:

                    formatted_message += (
                        f"\n\n"
                        f"Line {line_number}:\n"
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

        except Exception as e:

            return {
                "valid": False,
                "message": str(e),
                "line": None,
                "column": None,
                "error": str(e),
                "source_line": None,
                "pointer": "",
            }

    # ==========================================================
    # MAIN VALIDATION METHOD
    # ==========================================================

    @staticmethod
    def validate(
        code: str,
        language: str
    ):

        language = language.lower().strip()

        if language == "python":

            return SyntaxValidator.validate_python(
                code
            )

        elif language == "java":

            return SyntaxValidator.validate_java(
                code
            )

        return {
            "valid": False,
            "message": (
                "Unsupported programming language."
            ),
            "line": None,
            "column": None,
            "error": "Unsupported language",
            "source_line": None,
            "pointer": "",
        }