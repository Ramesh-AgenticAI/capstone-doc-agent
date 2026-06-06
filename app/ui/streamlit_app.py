import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Enterprise GenAI Assistant",
    layout="wide"
)

st.title("🤖 Enterprise Generative AI Assistant")

st.markdown("Upload enterprise documents and ask questions.")

# Session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar upload
with st.sidebar:

    st.header("📂 Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF/TXT/CSV/Excel",
        type=["pdf", "txt", "csv", "xlsx"]
    )

    if uploaded_file is not None:

        with st.spinner("Uploading and indexing document..."):

            response = requests.post(
                f"{API_URL}/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }
            )

            result = response.json()

            st.success("Document uploaded successfully!")
            st.json(result)

    st.divider()

    st.markdown("### Example Questions")

    st.info("""
What is dependency injection in .NET?

Explain SOLID principles.

What is async await in C#?

Difference between Task and Thread?

Explain boxing and unboxing.
""")


st.subheader("💬 Ask Questions")

query = st.chat_input("Ask question from uploaded documents...")

if query:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Call API
    with st.spinner("AI thinking..."):

        response = requests.get(
            f"{API_URL}/ask",
            params={"q": query}
        )

        result = response.json()

        answer = result.get("answer", "No answer found.")
        sources = result.get("sources", [])

        final_answer = answer

        # ----------------------------
        # FIXED SOURCES HANDLING
        # ----------------------------
        if sources:

            final_answer += "\n\n📚 Sources Used:"

            for source in sources:

                # CASE 1: source is dict (correct format)
                if isinstance(source, dict):
                    metadata = source.get("metadata", {})

                    source_name = metadata.get("source", "Unknown")
                    chunk_id = metadata.get("chunk_id", "N/A")

                    final_answer += f"\n- {source_name} (Chunk {chunk_id})"

                # CASE 2: source is string (your current issue)
                elif isinstance(source, str):
                    final_answer += f"\n- {source}"

                # CASE 3: unexpected type
                else:
                    final_answer += "\n- Unknown source format"

        # Store assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer
        })


# Render chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])