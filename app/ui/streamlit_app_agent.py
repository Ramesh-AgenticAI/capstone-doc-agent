import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Enterprise Agentic AI Assistant",
    layout="wide"
)

st.title("🧠 Enterprise Agentic AI Assistant")

st.markdown("""
Upload enterprise documents and ask intelligent questions using:

✅ Planner Agent  
✅ Retriever Agent  
✅ Reasoning Agent  
✅ Generator Agent  
✅ Validator Agent
""")

# --------------------------------------
# Session History
# --------------------------------------
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []


# --------------------------------------
# Sidebar Upload
# --------------------------------------
with st.sidebar:

    st.header("📂 Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF/TXT/CSV/Excel",
        type=["pdf", "txt", "csv", "xlsx"],
        key="agent_upload"
    )

    if uploaded_file is not None:

        with st.spinner(
            "Uploading and indexing document..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/upload-agent",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            uploaded_file.type
                        )
                    }
                )

                result = response.json()

                if result.get("success"):

                    st.success(
                        "Document uploaded "
                        "successfully!"
                    )

                    st.json(result)

                else:
                    st.error(
                        result.get(
                            "error",
                            "Upload failed"
                        )
                    )

            except Exception as ex:

                st.error(
                    f"Error: {str(ex)}"
                )

    st.divider()

    st.markdown(
        "### Agentic AI Example Questions"
    )

    st.info("""
Explain SOLID principles.

Explain C# palindrome program.

Move zeros to last position.

Difference between Task and Thread.

Explain JWT Authentication.

What is dependency injection?
""")


# --------------------------------------
# Chat Input
# --------------------------------------
st.subheader(
    "💬 Ask Agentic AI Questions"
)

query = st.chat_input(
    "Ask question from uploaded documents..."
)

if query:

    # Store user message
    st.session_state.agent_messages.append({
        "role": "user",
        "content": query
    })

    # API Call
    with st.spinner(
        "🤖 Agentic AI thinking..."
    ):

        try:

            response = requests.get(
                f"{API_URL}/ask-agent",
                params={"q": query}
            )

            result = response.json()

            answer = result.get(
                "answer",
                "No answer found."
            )

            workflow = result.get(
                "workflow",
                []
            )

            sources = result.get(
                "sources",
                []
            )

            final_answer = answer

            # --------------------------------------
            # Workflow Display
            # --------------------------------------
            if workflow:

                final_answer += (
                    "\n\n🧠 "
                    "**Agent Workflow Used:**\n"
                )

                for step in workflow:

                    final_answer += (
                        f"\n✅ {step.title()}"
                    )

            # --------------------------------------
            # Sources Display
            # --------------------------------------
            if sources:

                final_answer += (
                    "\n\n📚 "
                    "**Sources Used:**"
                )

                for source in sources:

                    if isinstance(
                        source,
                        dict
                    ):

                        metadata = source.get(
                            "metadata",
                            {}
                        )

                        source_name = (
                            metadata.get(
                                "source",
                                "Unknown"
                            )
                        )

                        chunk_id = (
                            metadata.get(
                                "chunk_id",
                                "N/A"
                            )
                        )

                        content_preview = (
                            source.get(
                                "content",
                                ""
                            )[:300]
                        )

                        final_answer += (
                            f"\n\n"
                            f"📄 {source_name}"
                            f" (Chunk {chunk_id})"
                            f"\n\n"
                            f"```text\n"
                            f"{content_preview}"
                            f"\n```"
                        )

                    elif isinstance(
                        source,
                        str
                    ):

                        final_answer += (
                            f"\n- {source}"
                        )

            # Store assistant message
            st.session_state.agent_messages.append({
                "role":
                "assistant",

                "content":
                final_answer
            })

        except Exception as ex:

            st.error(
                f"Error: {str(ex)}"
            )


# --------------------------------------
# Render Chat History
# --------------------------------------
for message in (
    st.session_state
    .agent_messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )