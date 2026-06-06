# from app.rag.llm import get_llm
# def reason(q,c):
#    return get_llm().invoke(c+"\n"+q).content

from typing import Optional
import logging

from app.rag.llm import get_llm

logger = logging.getLogger(__name__)


class ReasoningAgent:
    """
    Reasoning Agent for Enterprise RAG.

    Responsibilities:
    - Analyze retrieved context
    - Reason over documents
    - Generate grounded answers
    - Reduce hallucination
    - Handle missing context safely
    """

    def __init__(self):
        self.llm = get_llm()

    def build_prompt(self, query: str, context: str) -> str:
        """
        Build enterprise-level reasoning prompt.
        """

        prompt = f"""
You are an intelligent enterprise AI assistant.

Your task is to answer the user's question using ONLY the provided context.

RULES:
1. Use only the context below.
2. Do not hallucinate.
3. If answer is unavailable, say:
   "I could not find enough information in the retrieved documents."
4. Be concise but accurate.
5. If multiple sources disagree, mention uncertainty.
6. Explain reasoning step-by-step when appropriate.

=========================
RETRIEVED CONTEXT
=========================
{context}

=========================
USER QUESTION
=========================
{query}

=========================
ANSWER
=========================
"""
        return prompt

    def reason(self, query: str, context: str) -> str:
        """
        Run reasoning over retrieved context.

        Args:
            query (str): User query
            context (str): Retrieved RAG context

        Returns:
            str: Reasoned answer
        """

        try:
            if not query or not query.strip():
                return "Please provide a valid question."

            if not context or not context.strip():
                return (
                    "I could not find enough information "
                    "in the retrieved documents."
                )

            prompt = self.build_prompt(query, context)

            response = self.llm.invoke(prompt)

            if hasattr(response, "content"):
                answer = response.content
            else:
                answer = str(response)

            return answer.strip()

        except Exception as ex:
            logger.exception(f"Reasoning agent failed: {str(ex)}")
            return (
                "An error occurred while processing "
                "your request."
            )


# --------------------------------
# Functional wrapper
# --------------------------------

def reason(query: str, context: str) -> str:
    """
    Simple wrapper function.
    """
    agent = ReasoningAgent()
    return agent.reason(query, context)