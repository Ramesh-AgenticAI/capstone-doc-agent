import pandas as pd
def load_excel(p):
    xls=pd.ExcelFile(p)
    out=""
    for s in xls.sheet_names:
        df=pd.read_excel(p,sheet_name=s)
        out+=df.to_string(index=False)
    return out
