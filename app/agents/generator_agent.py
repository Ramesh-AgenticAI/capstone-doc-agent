import logging
from typing import Optional

from app.rag.llm import get_llm


logger = logging.getLogger(__name__)


class GeneratorAgent:
    """
    Generator Agent

    Responsibilities:
    - Generate final polished response
    - Improve readability
    - Summarize reasoning output
    - Format enterprise answer
    """

    def __init__(self):
        self.llm = get_llm()

    def build_prompt(
        self,
        query: str,
        reasoning_output: str,
        context: Optional[str] = None
    ) -> str:
        """
        Build generator prompt
        """

        prompt = f"""
You are an intelligent enterprise AI assistant.

Your task is to generate a professional,
well-structured, accurate response.

RULES:
1. Make answer clear and readable.
2. Use bullet points when needed.
3. Remove repetitive text.
4. Keep response relevant to user question.
5. If information is insufficient,
   mention limitations clearly.
6. Make answer concise but informative.

==================================
USER QUESTION
==================================
{query}

==================================
REASONING OUTPUT
==================================
{reasoning_output}

==================================
OPTIONAL CONTEXT
==================================
{context if context else "No additional context"}

==================================
FINAL RESPONSE
==================================
"""
        return prompt

    def generate(
        self,
        query: str,
        reasoning_output: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate polished final response
        """

        try:
            if not query.strip():
                return "Please enter a valid question."

            if not reasoning_output:
                return (
                    "Unable to generate a response "
                    "because reasoning output is empty."
                )

            prompt = self.build_prompt(
                query=query,
                reasoning_output=reasoning_output,
                context=context
            )

            response = self.llm.invoke(prompt)

            if hasattr(response, "content"):
                final_answer = response.content
            else:
                final_answer = str(response)

            return final_answer.strip()

        except Exception as ex:
            logger.exception(
                f"Generator Agent failed: {str(ex)}"
            )

            return (
                "An error occurred while generating "
                "the response."
            )


# -------------------------------------
# Functional Wrapper
# -------------------------------------

def generate(
    query: str,
    reasoning_output: str,
    context: Optional[str] = None
) -> str:
    """
    Simple wrapper function
    """

    agent = GeneratorAgent()

    return agent.generate(
        query=query,
        reasoning_output=reasoning_output,
        context=context
    )


# -------------------------------------
# Testing
# -------------------------------------

if __name__ == "__main__":

    query = "Explain JWT authentication in .NET 8"

    reasoning_output = """
JWT authentication uses token-based security.
In .NET 8, JwtBearer middleware validates
the token and secures APIs.
"""

    result = generate(
        query=query,
        reasoning_output=reasoning_output
    )

    print(result)