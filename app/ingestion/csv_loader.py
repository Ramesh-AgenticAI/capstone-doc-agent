import pandas as pd
def load_csv(p):
    return pd.read_csv(p).to_string(index=False)
