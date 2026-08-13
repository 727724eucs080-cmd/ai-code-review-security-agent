import streamlit as st

from rag.retriever import retrieve_documents
from llm.gemini_service import gemini_service


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Coding Assistant",
    page_icon="💬",
    layout="wide"
)


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("💬 Secure Coding Assistant")

st.write(
    "Ask questions about your submitted code, "
    "detected vulnerabilities, remediation, and secure coding practices."
)


# ==========================================================
# CHECK ANALYSIS
# ==========================================================

analysis_result = st.session_state.get(
    "analysis_result"
)

source_code = st.session_state.get(
    "source_code",
    ""
)

detected_language = st.session_state.get(
    "detected_language",
    ""
)


if not analysis_result:

    st.info(
        "Please submit and analyze code first."
    )

    st.stop()


# ==========================================================
# ANALYSIS INFORMATION
# ==========================================================

st.subheader("🔎 Current Analysis")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Language",
        detected_language.upper()
        if detected_language
        else "Unknown"
    )

with col2:

    statistics = analysis_result.get(
        "statistics",
        {}
    )

    st.metric(
        "Findings",
        statistics.get(
            "total",
            0
        )
    )

with col3:

    st.metric(
        "Risk Level",
        analysis_result.get(
            "risk_level",
            "Unknown"
        )
    )


# ==========================================================
# SHOW FINDINGS
# ==========================================================

st.divider()

st.subheader("🛡️ Findings From Your Code")


code_findings = (

    analysis_result

    .get(
        "code_analysis",
        {}
    )

    .get(
        "llm",
        {}
    )

    .get(
        "findings",
        []
    )
)


security_findings = (

    analysis_result

    .get(
        "security_analysis",
        {}
    )

    .get(
        "llm",
        {}
    )

    .get(
        "findings",
        []
    )
)


all_findings = (
    code_findings +
    security_findings
)


if all_findings:

    for index, finding in enumerate(
        all_findings,
        start=1
    ):

        if not isinstance(
            finding,
            dict
        ):
            continue

        title = finding.get(
            "title",
            "Finding"
        )

        severity = finding.get(
            "severity",
            "UNKNOWN"
        )

        with st.expander(
            f"{index}. {title} — {severity}"
        ):

            st.write(
                finding.get(
                    "description",
                    ""
                )
            )

            st.success(
                finding.get(
                    "recommendation",
                    ""
                )
            )

else:

    st.success(
        "No findings were detected."
    )


# ==========================================================
# CHAT HISTORY
# ==========================================================

if "assistant_history" not in st.session_state:

    st.session_state.assistant_history = []


for message in st.session_state.assistant_history:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ==========================================================
# USER QUESTION
# ==========================================================

question = st.chat_input(
    "Ask about your submitted code or findings..."
)


if question:

    # ------------------------------------------------------
    # Display user message
    # ------------------------------------------------------

    st.session_state.assistant_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # ======================================================
    # RAG RETRIEVAL
    # ======================================================

    with st.spinner(
        "Searching secure coding knowledge..."
    ):

        documents = retrieve_documents(
            question
        )


    if documents:

        knowledge_context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

    else:

        knowledge_context = (
            "No additional knowledge-base "
            "documents were retrieved."
        )


    # ======================================================
    # BUILD FINDINGS CONTEXT
    # ======================================================

    findings_context = ""

    if all_findings:

        for finding in all_findings:

            if not isinstance(
                finding,
                dict
            ):
                continue

            findings_context += (

                f"\nFinding: "
                f"{finding.get('title', '')}"

                f"\nSeverity: "
                f"{finding.get('severity', '')}"

                f"\nDescription: "
                f"{finding.get('description', '')}"

                f"\nRecommendation: "
                f"{finding.get('recommendation', '')}"

                "\n"

            )

    else:

        findings_context = (
            "No findings were detected."
        )


    # ======================================================
    # BUILD CODE CONTEXT
    # ======================================================

    code_context = source_code

    # Avoid sending an excessively large source file
    # to the local LLM.

    if len(code_context) > 12000:

        code_context = code_context[:12000]

        code_context += (
            "\n\n[Source code truncated]"
        )


    # ======================================================
    # ASSISTANT PROMPT
    # ======================================================

    prompt = f"""
You are the Secure Coding Assistant for an AI Code Review
and Security Analysis system.

You MUST answer the user's question specifically about
the submitted source code and its detected findings.

Do NOT give only generic secure-coding theory.

If the question refers to a finding, explain that exact
finding from the analysis result.

If the user asks why something is vulnerable, explain:

1. What is wrong in the submitted code.
2. Why it is a security or code-quality problem.
3. What an attacker or developer could do with it, when relevant.
4. How to fix the exact code.
5. Show a small secure-code example when useful.

If the submitted code does not contain the issue the user
is asking about, clearly say that.

Do not invent findings that are not present in the analysis.

--------------------------------------------------
DETECTED LANGUAGE
--------------------------------------------------

{detected_language}

--------------------------------------------------
SUBMITTED SOURCE CODE
--------------------------------------------------

{code_context}

--------------------------------------------------
FINDINGS DETECTED BY THE SYSTEM
--------------------------------------------------

{findings_context}

--------------------------------------------------
ADDITIONAL SECURE CODING KNOWLEDGE
--------------------------------------------------

{knowledge_context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
"""


    # ======================================================
    # GENERATE ANSWER
    # ======================================================

    with st.spinner(
        "Generating answer..."
    ):

        answer = gemini_service.invoke(
            prompt
    )


    # ======================================================
    # SAVE ASSISTANT MESSAGE
    # ======================================================

    st.session_state.assistant_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # ======================================================
    # DISPLAY ANSWER
    # ======================================================

    with st.chat_message(
        "assistant"
    ):

        st.write(answer)