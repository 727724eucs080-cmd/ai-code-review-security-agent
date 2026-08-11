# 🛡️ AI Code Review & Security Analysis Agent

An AI-powered code review system that analyzes source code for **code-quality issues and security vulnerabilities**, provides remediation recommendations, and allows developers to interact with their findings through a **Secure Coding Assistant**.

## 📌 Project Overview

Manual code review can be time-consuming and security issues may be overlooked during development.

This project automates the initial code-review process by combining **static analysis tools, AI-based analysis, and a multi-agent workflow**.

The system allows developers to upload or paste source code and automatically:

* Detect the programming language
* Validate syntax before analysis
* Analyze code quality
* Detect security vulnerabilities
* Classify findings by severity
* Generate remediation recommendations
* Generate a pull-request-style summary
* Discuss findings using the Secure Coding Assistant
* Export analysis reports

## 🎯 Objectives

* Automate the initial code-review process.
* Identify common code-quality problems.
* Detect potential security vulnerabilities.
* Provide understandable explanations for findings.
* Suggest practical remediation steps.
* Help developers learn secure coding practices.

## ✨ Key Features

### 🔍 Automatic Code Analysis

Users can upload a source-code file or paste code directly into the application.

The system automatically identifies the programming language and starts the appropriate analysis workflow.

### ✅ Syntax Validation

Syntax is checked **before the AI agents are executed**.

If syntax errors are detected, the analysis stops and the user is informed about the problem.

### 📊 Code Quality Analysis

The system identifies common code-quality issues such as:

* Naming problems
* Missing documentation
* Code smells
* Maintainability issues
* Poor coding practices

### 🛡️ Security Analysis

The security analysis identifies potential vulnerabilities such as:

* Hardcoded passwords
* Hardcoded secrets
* SQL injection risks
* Command injection risks
* Unsafe function usage
* Weak security practices

### 🛠️ Remediation

For each detected finding, the system provides:

* Issue
* Severity
* Description
* Recommended fix
* Developer action

### 💬 Secure Coding Assistant

Developers can ask questions about their **actual analysis findings** instead of receiving only general security concepts.

Example questions:

Why was this finding detected?

How can I fix this vulnerability?

What security risk does this finding create?

Show me a secure alternative.

Why is this finding classified as High severity?


### 📄 Report Generation

The application generates structured analysis reports that can be downloaded as:

* JSON
* PDF

### 📊 Dashboard

The dashboard provides a quick overview of:

* Overall score
* Security score
* Grade
* Risk level
* Finding severity
* Remediation recommendations

---

## 🔄 System Workflow


Source Code
    ↓
Language Detection
    ↓
Syntax Validation
    ↓
Code Analysis
    ↓
Security Analysis
    ↓
Finding Aggregation
    ↓
Remediation
    ↓
PR Summary
    ↓
Final Report
    ↓
Dashboard / Reports / Secure Coding Assistant


If syntax validation fails, the AI analysis is stopped.


## 🤖 Multi-Agent Architecture

The project uses a multi-agent workflow where different agents perform specific responsibilities.

### Code Analysis Agent

Analyzes code quality and maintainability issues.

### Security Analysis Agent

Identifies potential security vulnerabilities.

### Remediation Agent

Generates recommendations for fixing detected issues.

### PR Summary Agent

Creates a concise summary of the complete review.

The workflow is orchestrated using **LangGraph**.



## 🧰 Technology Stack

| Technology   | Purpose                      |
| ------------ | ---------------------------- |
| Python       | Core development             |
| Streamlit    | User interface               |
| LangGraph    | Agent workflow orchestration |
| LangChain    | AI/LLM integration           |
| Pylint       | Python code-quality analysis |
| Bandit       | Python security analysis     |
| Java `javac` | Java syntax validation       |
| Plotly       | Dashboard visualizations     |
| ReportLab    | PDF generation               |
| Git          | Version control              |


## 📁 Project Structure


AI-Code-Review-Security-Agent/
│
├── agents/
│   ├── code_analysis_agent.py
│   ├── security_analysis_agent.py
│   ├── remediation_agent.py
│   └── pr_summary_agent.py
│
├── graph/
│   └── workflow.py
│
├── validators/
│   └── syntax_validator.py
│
├── rag/
│   └── ...
│
├── reports/
│   ├── pdf_export.py
│   └── json_export.py
│
├── pages/
│   ├── Dashboard.py
│   ├── Code_Submission.py
│   ├── Secure_Coding_Assistant.py
│   ├── Reports.py
│   └── About.py
│
├── utils/
│   └── ui_helper.py
│
├── tests/
│   └── ...
│
├── app.py
├── requirements.txt
└── README.md




## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd AI-Code-Review-Security-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the required AI API key

Store API credentials using environment variables rather than hardcoding them in the source code.

---

## ▶️ Running the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application provides the following pages:

| Page                       | Purpose                       |
| -------------------------- | ----------------------------- |
| Dashboard                  | View overall analysis results |
| Code Submission & Analysis | Upload/paste and analyze code |
| Secure Coding Assistant    | Discuss detected findings     |
| Reports Generation         | View and download reports     |
| About                      | Project information           |

---

## 🧪 Example

A simple vulnerable example:

```python
password = "admin123"

def execute_query(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query
```

The system can identify issues such as:

* Hardcoded password
* SQL injection risk

and provide recommendations for improving the code.

---

## 📈 Analysis Output

The final analysis provides:

Overall Score
Security Score
Grade
Risk Level
Total Findings
Severity Distribution
Code Quality Findings
Security Findings
Remediation Recommendations
Pull Request Summary
```

---

## 🎓 What I Learned

Through this project, I gained practical experience in:

* Python application development
* Streamlit application development
* AI/LLM integration
* LangGraph-based workflows
* Multi-agent system design
* Static code analysis
* Secure coding concepts
* Vulnerability detection
* RAG-based assistance
* Report generation
* Debugging and testing
* Git and project version control

---

## 🚀 Future Enhancements

Some planned improvements include:

* Support for additional programming languages
* Faster analysis through optimized agent execution
* Improved severity scoring
* More comprehensive Java security analysis
* Line-level vulnerability highlighting
* Automatic secure-code suggestions
* GitHub repository integration
* Pull request integration
* CI/CD integration
* Improved report customization

---

## ⚠️ Limitations

The system is an AI-assisted code-review tool and should not replace professional security audits or manual code review.

AI and static-analysis results may contain false positives or miss certain vulnerabilities. Findings should therefore be reviewed before making production-level security decisions.

---

## 👤 Author

Harini M

AI Code Review & Security Analysis Agent

---

## 📄 License

This project was developed for **educational and internship purposes**.
