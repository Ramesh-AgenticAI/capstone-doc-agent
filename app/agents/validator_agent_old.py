# def validate(a,c):return True,a
class ValidatorAgent:

    def validate(
            self,
            answer,
            context
    ):

        """
        Validate generated response
        to reduce hallucinations
        and low-quality answers.
        """

        # Case 1:
        # No retrieved context
        if (
            not context
            or
            len(
                context.strip()
            ) == 0
        ):

            return (
                False,
                "No relevant information "
                "found in uploaded "
                "documents."
            )

        # Case 2:
        # Empty answer
        if (
            not answer
            or
            len(
                answer.strip()
            ) == 0
        ):

            return (
                False,
                "AI could not generate "
                "a response."
            )

        # Case 3:
        # Very short response
        if (
            len(
                answer.strip()
            ) < 10
        ):

            return (
                False,
                "Generated answer "
                "is too short."
            )

        # Case 4:
        # Hallucination detection
        blocked_phrases = [

            "i don't know",

            "not sure",

            "cannot determine",

            "insufficient information",

            "unknown"
        ]

        lower_answer = (
            answer.lower()
        )

        for phrase in (
                blocked_phrases
        ):

            if (
                phrase
                in lower_answer
            ):

                return (
                    False,
                    "Answer validation "
                    "failed due to "
                    "insufficient confidence."
                )

        # Case 5:
        # Validate against context
        similarity_score = (
            self
            .check_context_match(
                answer,
                context
            )
        )

        if (
            similarity_score < 0.10
        ):

            return (
                False,
                "Generated answer "
                "does not match "
                "retrieved context."
            )

        # Passed validation
        return (
            True,
            answer
        )

    def check_context_match(
            self,
            answer,
            context
    ):

        """
        Basic grounding validation.
        Checks overlap between
        answer and retrieved
        context.
        """

        answer_words = set(
            answer.lower().split()
        )

        context_words = set(
            context.lower().split()
        )

        common_words = (
            answer_words
            .intersection(
                context_words
            )
        )

        if (
            len(answer_words)
            == 0
        ):

            return 0

        score = (
            len(common_words)
            /
            len(answer_words)
        )

        return score
