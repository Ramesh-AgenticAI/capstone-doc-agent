import os
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.txt_loader import load_txt
from app.ingestion.csv_loader import load_csv
from app.ingestion.excel_loader import load_excel

def process_document(p):
    ext=os.path.splitext(p)[1]
    if ext==".pdf":return load_pdf(p)
    if ext==".txt":return load_txt(p)
    if ext==".csv":return load_csv(p)
    if ext==".xlsx":return load_excel(p)
    return ""
