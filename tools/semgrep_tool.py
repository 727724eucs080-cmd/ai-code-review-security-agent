import json
import os
import subprocess
import tempfile


class SemgrepTool:

    @staticmethod
    def scan(code: str, language: str = "java"):

        temp_path = None

        try:

            language = language.lower().strip()

            extension = {
                "java": ".java",
                "python": ".py",
                "javascript": ".js",
                "typescript": ".ts",
                "c": ".c",
                "cpp": ".cpp",
                "go": ".go"
            }.get(language, ".txt")

            with tempfile.NamedTemporaryFile(
                suffix=extension,
                delete=False,
                mode="w",
                encoding="utf-8"
            ) as temp:

                temp.write(code)
                temp_path = temp.name

            result = subprocess.run(
                [
                    "semgrep",
                    "--config=auto",
                    "--json",
                    "--quiet",
                    temp_path
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )

            if not result.stdout.strip():

                return {
                    "results": [],
                    "errors": []
                }

            try:

                data = json.loads(result.stdout)

            except json.JSONDecodeError:

                return {
                    "error": "Unable to parse Semgrep output.",
                    "results": [],
                    "errors": []
                }

            results = data.get("results", [])

            normalized = []
            seen = set()

            for finding in results:

                extra = finding.get("extra", {})

                start = finding.get("start", {})
                end = finding.get("end", {})

                line = start.get("line", 0)
                end_line = end.get("line", line)

                message = extra.get(
                    "message",
                    "Semgrep security finding."
                )

                severity = extra.get(
                    "severity",
                    "WARNING"
                )

                metadata = extra.get(
                    "metadata",
                    {}
                )

                cwe = metadata.get(
                    "cwe",
                    []
                )

                owasp = metadata.get(
                    "owasp",
                    []
                )

                vulnerability_class = metadata.get(
                    "vulnerability_class",
                    []
                )

                category = metadata.get(
                    "category",
                    "security"
                )

                rule_id = finding.get(
                    "check_id",
                    ""
                )

                dedup_key = (
                    language,
                    line,
                    end_line,
                    message
                )

                if dedup_key in seen:
                    continue

                seen.add(dedup_key)

                normalized.append(
                    {
                        "rule_id": rule_id,
                        "title": (
                            vulnerability_class[0]
                            if vulnerability_class
                            else message
                        ),
                        "severity": severity,
                        "category": category,
                        "message": message,
                        "line": line,
                        "end_line": end_line,
                        "cwe": cwe,
                        "owasp": owasp,
                        "path": finding.get(
                            "path",
                            temp_path
                        )
                    }
                )

            return {
                "results": normalized,
                "errors": data.get(
                    "errors",
                    []
                ),
                "version": data.get(
                    "version"
                )
            }

        except subprocess.TimeoutExpired:

            return {
                "error": "Semgrep scan timed out.",
                "results": [],
                "errors": []
            }

        except FileNotFoundError:

            return {
                "error": "Semgrep executable was not found.",
                "results": [],
                "errors": []
            }

        except Exception as e:

            return {
                "error": str(e),
                "results": [],
                "errors": []
            }

        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)