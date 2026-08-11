import streamlit as st


def severity_badge(severity):

    severity = severity.upper()

    if severity == "CRITICAL":

        st.error(severity)

    elif severity == "HIGH":

        st.error(severity)

    elif severity == "MEDIUM":

        st.warning(severity)

    elif severity == "LOW":

        st.info(severity)

    else:

        st.success(severity)