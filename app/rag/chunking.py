# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
def create_chunks(t):
    return RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150).split_text(t)
