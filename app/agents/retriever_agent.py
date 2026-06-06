# from app.rag.retriever import search_documents
# def retrieve(q):
#    docs=search_documents(q)
#    return "\n".join([d.page_content for d in docs]),docs

from typing import List, Tuple, Dict, Any, Optional
import logging

from app.rag.retriever import search_documents

logger = logging.getLogger(__name__)


class RetrieverAgent:
    """
    Retriever Agent for RAG pipeline.
    Responsible for fetching relevant documents based on user query.
    """

    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def retrieve(self, query: str) -> Tuple[str, List[Any]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query (str): user question

        Returns:
            Tuple[str, List[Document]]: 
                - combined context string
                - raw document objects
        """
        try:
            if not query or not query.strip():
                logger.warning("Empty query received in retriever")
                return "", []

            # Step 1: fetch documents
            docs = search_documents(query)

            if not docs:
                logger.info(f"No documents found for query: {query}")
                return "", []

            # Step 2: optionally limit top_k results
            docs = docs[: self.top_k]

            # Step 3: build context safely
            context_parts = []

            for i, doc in enumerate(docs):
                content = getattr(doc, "page_content", "")

                if not content:
                    continue

                # Optional metadata handling
                metadata = getattr(doc, "metadata", {})
                source = metadata.get("source", "unknown")

                formatted = f"[Doc {i+1} | Source: {source}]\n{content}"
                context_parts.append(formatted)

            context = "\n\n".join(context_parts)

            logger.info(f"Retrieved {len(context_parts)} documents for query")

            return context, docs

        except Exception as e:
            logger.exception(f"Retriever error: {str(e)}")
            return "", []


# -------------------------
# Simple functional wrapper (if you don't want class)
# -------------------------

def retrieve(query: str) -> Tuple[str, List[Any]]:
    agent = RetrieverAgent()
    return agent.retrieve(query)