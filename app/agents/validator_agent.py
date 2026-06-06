import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class ValidatorAgent:
    """
    Validator Agent

    Responsibilities:
    - Validate generated answer
    - Check confidence
    - Detect hallucination
    - Ensure answer relevance
    """

    def __init__(self):
        pass

    def validate(
        self,
        answer: str,
        context: str
    ) -> Tuple[bool, str]:
        """
        Validate generated answer.

        Returns:
            (is_valid, validated_answer)
        """

        try:

            # Empty answer check
            if not answer or not answer.strip():

                return (
                    False,
                    "Generated answer is empty."
                )

            # No context available
            if not context or not context.strip():

                return (
                    True,
                    answer
                )

            # Simple relevance check
            context_words = set(
                context.lower().split()
            )

            answer_words = set(
                answer.lower().split()
            )

            overlap = (
                len(
                    context_words.intersection(
                        answer_words
                    )
                )
            )

            confidence_score = (
                overlap /
                max(
                    len(answer_words),
                    1
                )
            )

            logger.info(
                f"Validation score: "
                f"{confidence_score}"
            )

            # Confidence threshold
            if confidence_score < 0.10:

                warning = (
                    "\n\n⚠ Low confidence "
                    "response detected."
                )

                return (
                    False,
                    answer + warning
                )

            return (
                True,
                answer
            )

        except Exception as ex:

            logger.exception(
                f"Validator failed: "
                f"{str(ex)}"
            )

            return (
                False,
                "Validation failed."
            )


# -----------------------------
# Functional Wrapper
# -----------------------------

def validate(
    answer: str,
    context: str
):
    """
    Simple wrapper
    """

    agent = ValidatorAgent()

    return agent.validate(
        answer,
        context
    )


# -----------------------------
# Testing
# -----------------------------
if __name__ == "__main__":

    context = """
    JWT authentication uses
    bearer tokens in .NET 8.
    """

    answer = """
    JWT authentication uses
    bearer tokens.
    """

    valid, response = validate(
        answer,
        context
    )

    print(valid)
    print(response)