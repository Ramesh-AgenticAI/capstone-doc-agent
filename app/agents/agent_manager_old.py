from app.agents.retriever_agent import retrieve
from app.agents.reasoning_agent import reason
from app.agents.validator_agent import validate

def run_agent_system(q):
    c,docs=retrieve(q)
    a=reason(q,c)
    v,_=validate(a,c)
    return {"answer":v,"sources":[d.page_content for d in docs]}
