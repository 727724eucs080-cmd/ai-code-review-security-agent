import streamlit as st

st.set_page_config(
    page_title="AI Code Review & Security Analysis",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code Review & Security Analysis Agent")

st.markdown("""
Welcome to the **AI Code Review & Security Analysis Agent**.

This application uses AI and static analysis tools to review source code,
detect vulnerabilities, suggest fixes, and generate professional reports.

---

### Features

- ✅ Syntax Validation
- 🔍 AI Code Quality Review
- 🛡 Security Vulnerability Detection
- 🛠 AI Remediation Suggestions
- 📝 Pull Request Summary Generation
- 📄 Download Analysis Reports
- 💬 Secure Coding Assistant (RAG)

---

### Workflow

1. Open **Code Submission**
2. Upload or paste your source code
3. Click **Analyze Code**
4. View results in **Dashboard**
5. Download reports from **Reports**
6. Ask secure coding questions in **Secure Coding Assistant**
""")

st.success("Select a page from the left sidebar to begin.")