import streamlit as st
import requests

st.title("GenAI Assistant")

file=st.file_uploader("Upload")
if file:
    r=requests.post("http://localhost:8000/upload",files={"file":file})
    st.write(r.json())

q=st.text_input("Ask")
if st.button("ask"):
    r=requests.get("http://localhost:8000/ask",params={"q":q})
    st.write(r.json())
