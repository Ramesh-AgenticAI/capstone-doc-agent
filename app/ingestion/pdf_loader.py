import pdfplumber
def load_pdf(p):
    text=""
    with pdfplumber.open(p) as pdf:
        for page in pdf.pages:
            t=page.extract_text()
            if t:text+=t+"\n"
    return text
