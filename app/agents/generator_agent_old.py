class GeneratorAgent:

    def generate_response(
            self,
            answer,
            sources
    ):

        """
        Formats final enterprise response
        before sending to UI/API
        """

        formatted_sources = []

        for source in sources:

            formatted_sources.append(
                {
                    "source":
                    source.get(
                        "source",
                        "Unknown"
                    ),

                    "chunk_id":
                    source.get(
                        "chunk_id",
                        "N/A"
                    )
                }
            )

        response = {
            "status":
            "success",

            "answer":
            answer,

            "sources":
            formatted_sources
        }

        return response