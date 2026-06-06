# def plan_task(q):return "rag"
import logging
from typing import Dict, Any


logger = logging.getLogger(__name__)


class PlannerAgent:
    """
    Planner Agent

    Responsibilities:
    - Understand user intent
    - Decide execution strategy
    - Route tasks to correct agents
    - Enable agentic workflows
    """

    def __init__(self):
        pass

    def detect_query_type(self, query: str) -> str:
        """
        Detect query type.
        """

        query = query.lower()

        rag_keywords = [
            "document",
            "pdf",
            "knowledge base",
            "company policy",
            "retrieved",
            "explain from file",
            "uploaded file",
            "search"
        ]

        reasoning_keywords = [
            "analyze",
            "compare",
            "difference",
            "why",
            "how",
            "architecture",
            "design",
            "strategy",
            "reason"
        ]

        greeting_keywords = [
            "hello",
            "hi",
            "hey"
        ]

        if any(word in query for word in greeting_keywords):
            return "chat"

        if any(word in query for word in rag_keywords):
            return "rag"

        if any(word in query for word in reasoning_keywords):
            return "reasoning"

        return "general"

    def create_execution_plan(self, query: str) -> Dict[str, Any]:
        """
        Create execution plan for query.
        """

        task_type = self.detect_query_type(query)

        if task_type == "rag":
            return {
                "task_type": "rag",
                "use_retriever": True,
                "use_reasoning": True,
                "use_generator": True,
                "use_validator": True,
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
                "use_retriever": False,
                "use_reasoning": True,
                "use_generator": True,
                "use_validator": True,
                "workflow": [
                    "reason",
                    "generate",
                    "validate"
                ]
            }

        elif task_type == "chat":
            return {
                "task_type": "chat",
                "use_retriever": False,
                "use_reasoning": False,
                "use_generator": True,
                "use_validator": False,
                "workflow": [
                    "generate"
                ]
            }

        return {
            "task_type": "general",
            "use_retriever": False,
            "use_reasoning": True,
            "use_generator": True,
            "use_validator": True,
            "workflow": [
                "reason",
                "generate",
                "validate"
            ]
        }

    def plan_task(self, query: str) -> Dict[str, Any]:
        """
        Main planner method.
        """

        try:
            if not query.strip():
                return {
                    "task_type": "invalid",
                    "workflow": []
                }

            plan = self.create_execution_plan(query)

            logger.info(
                f"Task planned successfully: "
                f"{plan['task_type']}"
            )

            return plan

        except Exception as ex:
            logger.exception(
                f"Planner failed: {str(ex)}"
            )

            return {
                "task_type": "fallback",
                "workflow": [
                    "generate"
                ]
            }


# --------------------------
# Functional Wrapper
# --------------------------

def plan_task(query: str):
    """
    Simple wrapper function
    """

    planner = PlannerAgent()
    return planner.plan_task(query)


# --------------------------
# Testing
# --------------------------

if __name__ == "__main__":

    test_queries = [
        "Explain JWT authentication from uploaded PDF",
        "Compare Angular vs React",
        "Hello",
        "How microservices work?"
    ]

    for q in test_queries:
        print("=" * 50)
        print("Question:", q)
        print(plan_task(q))
