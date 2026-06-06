from app.rag.chunking import create_chunks
from app.rag.embedding import get_embedding
from langchain_community.vectorstores import Chroma

DB="chroma_db"

def index_document(text, name):
    chunks=create_chunks(text)
    db=Chroma.from_texts(chunks,get_embedding(),persist_directory=DB)
    db.persist()
    return len(chunks)

def search_documents(q,k=3):
    db=Chroma(persist_directory=DB,embedding_function=get_embedding())
    return db.similarity_search(q,k=k)
