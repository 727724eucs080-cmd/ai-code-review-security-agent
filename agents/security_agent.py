import re

from tools.ollama_tool import OllamaTool
from tools.bandit_tool import BanditTool


class SecurityAgent:

    def analyze(self, code: str, language: str):

        language = language.lower().strip()

        # ==========================================================
        # PYTHON SECURITY ANALYSIS
        # ==========================================================

        if language == "python":

            bandit_report = BanditTool.scan(code)

            prompt = f"""
You are a senior Python application security engineer.

Analyze the following Python code for security vulnerabilities.

Use the Bandit findings as supporting evidence.

Return ONLY valid JSON in this format:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "why this is dangerous",
            "recommendation": "how to fix it"
        }}
    ]
}}

Python Code:
{code}

Bandit Report:
{bandit_report}
"""

            response = OllamaTool.generate(prompt)

            response = response.replace("```json", "")
            response = response.replace("```", "").strip()

            try:
                import json
                llm = json.loads(response)

            except Exception:
                llm = {
                    "summary": "Unable to parse security analysis.",
                    "findings": []
                }

            return {
                "bandit": bandit_report,
                "llm": llm
            }

        # ==========================================================
        # JAVA SECURITY ANALYSIS
        # ==========================================================

        if language == "java":

            findings = []

            # ------------------------------------------------------
            # 1. Hardcoded password
            # ------------------------------------------------------

            password_pattern = re.compile(
                r'(?i)(password|passwd|pwd)\s*=\s*"[^"]+"'
            )

            if password_pattern.search(code):

                findings.append({
                    "title": "Hardcoded Password",
                    "severity": "HIGH",
                    "description": (
                        "A password is directly stored as a string "
                        "literal in the Java source code."
                    ),
                    "recommendation": (
                        "Remove the hardcoded password and use "
                        "environment variables, a secrets manager, "
                        "or another secure credential store."
                    )
                })

            # ------------------------------------------------------
            # 2. Hardcoded API key / secret
            # ------------------------------------------------------

            secret_pattern = re.compile(
                r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)'
                r'\s*=\s*"[^"]+"'
            )

            if secret_pattern.search(code):

                findings.append({
                    "title": "Hardcoded Secret",
                    "severity": "HIGH",
                    "description": (
                        "A sensitive key or token appears to be "
                        "hardcoded in the source code."
                    ),
                    "recommendation": (
                        "Store secrets outside the source code using "
                        "environment variables or a secure secrets manager."
                    )
                })

            # ------------------------------------------------------
            # 3. SQL Injection risk
            # ------------------------------------------------------

            sql_pattern = re.compile(
                r'(?i)(executeQuery|executeUpdate|prepareStatement)'
                r'\s*\(\s*[^)]*\+'
            )

            if sql_pattern.search(code):

                findings.append({
                    "title": "SQL Injection Risk",
                    "severity": "CRITICAL",
                    "description": (
                        "SQL statements appear to be constructed using "
                        "string concatenation, which can allow attacker "
                        "controlled input to modify the query."
                    ),
                    "recommendation": (
                        "Use parameterized queries or prepared statements "
                        "with bound parameters."
                    )
                })

            # ------------------------------------------------------
            # 4. Runtime command execution
            # ------------------------------------------------------

            command_pattern = re.compile(
                r'(?i)(Runtime\.getRuntime\(\)\.exec|'
                r'ProcessBuilder\s*\()'
            )

            if command_pattern.search(code):

                findings.append({
                    "title": "Command Execution Risk",
                    "severity": "HIGH",
                    "description": (
                        "The code executes operating-system commands. "
                        "If attacker-controlled input reaches this code, "
                        "command injection may occur."
                    ),
                    "recommendation": (
                        "Avoid executing shell commands where possible. "
                        "If required, validate input strictly and avoid "
                        "passing untrusted input to command execution."
                    )
                })

            # ------------------------------------------------------
            # 5. Weak cryptography
            # ------------------------------------------------------

            weak_crypto_pattern = re.compile(
                r'(?i)MessageDigest\.getInstance\s*\(\s*"'
                r'(MD5|SHA-1)"'
            )

            if weak_crypto_pattern.search(code):

                findings.append({
                    "title": "Weak Cryptographic Algorithm",
                    "severity": "HIGH",
                    "description": (
                        "The code uses MD5 or SHA-1, which are not "
                        "recommended for secure cryptographic purposes."
                    ),
                    "recommendation": (
                        "Use modern cryptographic algorithms such as "
                        "SHA-256 or stronger algorithms appropriate "
                        "for the security requirement."
                    )
                })

            # ------------------------------------------------------
            # LLM contextual Java analysis
            # ------------------------------------------------------

            prompt = f"""
You are a senior Java application security engineer.

Analyze this Java code for security vulnerabilities.

Focus on:

- Hardcoded credentials
- SQL injection
- Command injection
- Weak cryptography
- Authentication problems
- Authorization problems
- Unsafe deserialization
- Path traversal
- Sensitive information exposure
- Insecure input handling

Return ONLY valid JSON:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "specific explanation",
            "recommendation": "specific fix"
        }}
    ]
}}

Java Code:
{code}
"""

            response = OllamaTool.generate(prompt)

            response = response.replace("```json", "")
            response = response.replace("```", "").strip()

            try:
                import json

                llm = json.loads(response)

            except Exception:

                llm = {
                    "summary": "Java security analysis completed.",
                    "findings": []
                }

            # ------------------------------------------------------
            # Add LLM findings without losing static findings
            # ------------------------------------------------------

            llm_findings = llm.get(
                "findings",
                []
            )

            if isinstance(llm_findings, list):

                existing_titles = {
                    item["title"].lower()
                    for item in findings
                }

                for finding in llm_findings:

                    if not isinstance(
                        finding,
                        dict
                    ):
                        continue

                    title = str(
                        finding.get(
                            "title",
                            ""
                        )
                    )

                    if title.lower() not in existing_titles:

                        findings.append(finding)

            # ------------------------------------------------------
            # Final Java result
            # ------------------------------------------------------

            if findings:

                summary = (
                    f"Java security analysis identified "
                    f"{len(findings)} potential security issue(s)."
                )

            else:

                summary = (
                    "No obvious Java security vulnerabilities "
                    "were detected by the configured security checks."
                )

            return {
                "static": {
                    "findings": findings
                },
                "llm": {
                    "summary": summary,
                    "findings": findings
                }
            }

        # ==========================================================
        # UNSUPPORTED LANGUAGE
        # ==========================================================

        return {
            "static": {
                "findings": []
            },
            "llm": {
                "summary": "Unsupported programming language.",
                "findings": []
            }
        }


security_agent = SecurityAgent()

