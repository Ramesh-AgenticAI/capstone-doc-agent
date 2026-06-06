from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import os

# -------------------------
# Existing RAG Imports
# -------------------------
from app.rag.retriever import (
    index_document
)

from app.rag.rag_pipeline import (
    generate_answer
)

# -------------------------
# Agentic AI Imports
# -------------------------
from app.agents.agent_manager import (
    run_agent_system
)

router = APIRouter()


# ==========================================
# ROOT
# ==========================================
@router.get("/")
def root():

    return {
        "message":
        "Enterprise GenAI API Running"
    }


# ==========================================
# EXISTING RAG UPLOAD
# ==========================================
@router.post("/upload")
async def upload(
    file: UploadFile = File(...)
):

    try:
        os.makedirs(
            "uploads",
            exist_ok=True
        )

        content = await file.read()

        path = (
            f"uploads/"
            f"{file.filename}"
        )

        with open(
            path,
            "wb"
        ) as f:
            f.write(content)

        from app.ingestion.document_processor import (
            process_document
        )

        text = process_document(
            path
        )

        chunks = index_document(
            text,
            file.filename
        )

        return {
            "success": True,
            "message":
            "File uploaded successfully",

            "chunks":
            chunks
        }

    except Exception as ex:

        return {
            "success": False,
            "error": str(ex)
        }


# ==========================================
# EXISTING RAG ASK
# ==========================================
@router.get("/ask")
def ask(q: str):

    try:
        result = generate_answer(q)

        return {
            "success": True,
            "question": q,
            "answer": result
        }

    except Exception as ex:

        return {
            "success": False,
            "error": str(ex)
        }


# ==========================================
# AGENT ROOT
# ==========================================
@router.get("/agent-root")
def agent_root():

    return {
        "message":
        "Agentic AI API Running"
    }


# ==========================================
# AGENTIC AI UPLOAD
# ==========================================
@router.post("/upload-agent")
async def upload_agent(
    file: UploadFile = File(...)
):

    try:
        os.makedirs(
            "uploads",
            exist_ok=True
        )

        content = await file.read()

        path = (
            f"uploads/"
            f"{file.filename}"
        )

        with open(
            path,
            "wb"
        ) as f:
            f.write(content)

        from app.ingestion.document_processor import (
            process_document
        )

        text = process_document(
            path
        )

        chunks = index_document(
            text,
            file.filename
        )

        return {
            "success": True,
            "message":
            "Document uploaded "
            "for Agentic AI",

            "chunks":
            chunks
        }

    except Exception as ex:

        return {
            "success": False,
            "error": str(ex)
        }


# ==========================================
# AGENTIC AI ASK
# ==========================================
@router.get("/ask-agent")
def ask_agent(q: str):

    try:
        result = run_agent_system(q)

        return {
            "success":
            result["success"],

            "question":
            q,

            "answer":
            result["answer"],

            "workflow":
            result["workflow"],

            "sources":
            result["sources"]
        }

    except Exception as ex:

        return {
            "success": False,
            "error": str(ex)
        }