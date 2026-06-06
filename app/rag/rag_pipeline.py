from app.rag.retriever import search_documents
from app.rag.llm import get_llm
from app.rag.prompt import build_prompt

def generate_answer(q):
    docs=search_documents(q)
    context="\n".join([d.page_content for d in docs])
    llm=get_llm()
    res=llm.invoke(build_prompt(context,q))
    return {"answer":res.content,"sources":[d.page_content for d in docs]}
