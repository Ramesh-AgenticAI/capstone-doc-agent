import logging
from typing import Dict, Any

from app.agents.planner_agent import plan_task
from app.agents.retriever_agent import retrieve
from app.agents.reasoning_agent import reason
from app.agents.generator_agent import generate
from app.agents.validator_agent import validate


logger = logging.getLogger(__name__)


class AgentManager:
    """
    Agent Manager

    Responsibilities:
    - Orchestrate all agents
    - Execute planner workflow
    - Run retrieval, reasoning,
      generation, validation
    - Return final structured output
    """

    def __init__(self):
        pass

    def run_agent_system(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Main agentic workflow.
        """

        try:
            if not query.strip():
                return {
                    "success": False,
                    "answer": "Please enter a valid question.",
                    "sources": [],
                    "workflow": []
                }

            # -----------------------------
            # Step 1: Plan Task
            # -----------------------------
            plan = plan_task(query)

            workflow = plan.get("workflow", [])

            logger.info(
                f"Workflow selected: {workflow}"
            )

            context = ""
            docs = []
            reasoning_output = ""
            generated_answer = ""
            final_answer = ""

            # -----------------------------
            # Step 2: Retrieval
            # -----------------------------
            if "retrieve" in workflow:
                logger.info("Running Retriever Agent")

                context, docs = retrieve(query)

            # -----------------------------
            # Step 3: Reasoning
            # -----------------------------
            if "reason" in workflow:
                logger.info("Running Reasoning Agent")

                reasoning_output = reason(
                    query,
                    context
                )

            # -----------------------------
            # Step 4: Generation
            # -----------------------------
            if "generate" in workflow:
                logger.info("Running Generator Agent")

                generated_answer = generate(
                    query=query,
                    reasoning_output=reasoning_output,
                    context=context
                )

            # -----------------------------
            # Step 5: Validation
            # -----------------------------
            if "validate" in workflow:
                logger.info("Running Validator Agent")

                is_valid, validated_answer = validate(
                    generated_answer,
                    context
                )

                final_answer = validated_answer

                if not is_valid:
                    final_answer += (
                        "\n\n⚠ Warning: "
                        "Response confidence is low."
                    )

            else:
                final_answer = generated_answer

            # -----------------------------
            # Format Sources
            # -----------------------------
            sources = []

            for doc in docs:
                try:
                    source_info = {
                        "content": getattr(
                            doc,
                            "page_content",
                            ""
                        ),
                        "metadata": getattr(
                            doc,
                            "metadata",
                            {}
                        )
                    }

                    sources.append(source_info)

                except Exception:
                    continue

            return {
                "success": True,
                "query": query,
                "answer": final_answer,
                "sources": sources,
                "workflow": workflow
            }

        except Exception as ex:
            logger.exception(
                f"Agent system failed: {str(ex)}"
            )

            return {
                "success": False,
                "query": query,
                "answer": (
                    "An unexpected error "
                    "occurred."
                ),
                "sources": [],
                "workflow": []
            }


# -----------------------------------
# Functional Wrapper
# -----------------------------------

def run_agent_system(
    query: str
) -> Dict[str, Any]:
    """
    Simple wrapper function.
    """

    manager = AgentManager()

    return manager.run_agent_system(query)


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    question = (
        "Explain JWT authentication "
        "from uploaded PDF"
    )

    result = run_agent_system(
        question
    )

    print("\nFinal Result\n")
    print(result["answer"])

    print("\nWorkflow Used:")
    print(result["workflow"])

    print("\nSources Count:")
    print(len(result["sources"]))