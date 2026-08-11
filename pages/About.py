import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About")

st.markdown("""
# AI Code Review & Security Analysis Agent

## Project Overview

The AI Code Review & Security Analysis Agent is an intelligent software
quality assurance platform that automates source code review using
Artificial Intelligence, Static Code Analysis, and Retrieval-Augmented
Generation (RAG).

The system helps developers identify code quality issues,
security vulnerabilities, and provides remediation suggestions
along with an automatically generated Pull Request summary.

---

## Technologies Used

### Backend

- Python
- LangGraph
- LangChain
- Ollama
- FAISS
- Pylint
- Bandit

### Frontend

- Streamlit

### AI Models

- Qwen 2.5 Coder

### Security Standards

- OWASP Top 10
- Python Secure Coding Guidelines
- Java Secure Coding Guidelines

---

## Modules

- Syntax Validation
- Code Analysis Agent
- Security Analysis Agent
- Remediation Agent
- PR Summary Agent
- Report Generator
- Secure Coding Assistant

---

## Developed As

Academic Major Project

AI Code Review & Security Analysis Agent
""")