import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class PlannerAgent:
    """
    Planner Agent
    Responsible for selecting workflow.
    """

    def __init__(self):
        pass

    def detect_query_type(
        self,
        query: str
    ) -> str:
        """
        Detect query type intelligently.
        """

        query = query.lower()

        # -------------------------
        # Greeting Keywords
        # -------------------------
        greeting_keywords = [
            "hello",
            "hi",
            "hey"
        ]

        # -------------------------
        # RAG Keywords
        # -------------------------
        rag_keywords = [
            "document",
            "pdf",
            "uploaded",
            "file",
            "search",
            "coding",
            "interview",
            "program",
            "code",
            "algorithm",
            "c#",
            ".net",
            "palindrome",
            "fibonacci",
            "swap",
            "move zero",
            "reverse string",
            "factorial",
            "prime",
            "anagram",
            "armstrong",
            "bubble sort",
            "array",
            "string"
        ]

        # -------------------------
        # Reasoning Keywords
        # -------------------------
        reasoning_keywords = [
            "analyze",
            "compare",
            "difference",
            "why",
            "how",
            "architecture",
            "design",
            "strategy",
            "microservices",
            "system design"
        ]

        # Greeting
        if any(
            word in query
            for word in greeting_keywords
        ):
            return "chat"

        # Prioritize RAG
        if any(
            word in query
            for word in rag_keywords
        ):
            return "rag"

        # Reasoning
        if any(
            word in query
            for word in reasoning_keywords
        ):
            return "reasoning"

        # Default fallback
        return "rag"

    def create_execution_plan(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Create execution plan.
        """

        task_type = self.detect_query_type(
            query
        )

        if task_type == "rag":
            return {
                "task_type": "rag",
                "workflow": [
                    "retrieve",
                    "reason",
                    "generate",
                    "validate"
                ]
            }

        elif task_type == "reasoning":
            return {
                "task_type": "reasoning",
                "workflow": [
                    "reason",
                    "generate",
                    "validate"
                ]
            }

        elif task_type == "chat":
            return {
                "task_type": "chat",
                "workflow": [
                    "generate"
                ]
            }

        return {
            "task_type": "general",
            "workflow": [
                "retrieve",
                "reason",
                "generate",
                "validate"
            ]
        }

    def plan_task(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Main planner function.
        """

        try:

            if not query.strip():
                return {
                    "task_type":
                    "invalid",

                    "workflow":
                    []
                }

            plan = (
                self
                .create_execution_plan(
                    query
                )
            )

            logger.info(
                f"Planned task: "
                f"{plan['task_type']}"
            )

            return plan

        except Exception as ex:

            logger.exception(
                f"Planner failed: "
                f"{str(ex)}"
            )

            return {
                "task_type":
                "fallback",

                "workflow":
                [
                    "generate"
                ]
            }


# --------------------------------
# Functional Wrapper
# --------------------------------
def plan_task(query: str):

    planner = PlannerAgent()

    return planner.plan_task(
        query
    )