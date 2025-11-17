import pandas as pd
from app_categoria import map_categoria, CATEGORY_MAP

# Load your CSV -------------------------------------------------------

df = pd.read_csv("data/relatorio_faturamento.csv")
df["Descricao"] = df["Descricao"].astype(str)

# Apply categorization -------------------------------------------------

df["Categoria"] = df["Descricao"].apply(map_categoria)

# Report 1: Items that fall into "Outros" ------------------------------

df_outros = df[df["Categoria"] == "Outros"]
df_outros.to_csv("scan_outros.csv", index=False)

# Report 2: Items matching multiple categories -------------------------

def find_all_matches(text):
    text = text.upper()
    matches = []
    for _, row in CATEGORY_MAP.iterrows():
        if row["pattern"] in text:
            matches.append(row["categoria"])
    return matches

df["AllMatches"] = df["Descricao"].apply(find_all_matches)
df_multi = df[df["AllMatches"].apply(lambda x: len(x) > 1)]
df_multi.to_csv("scan_multimatch.csv", index=False)

# Report 3: Summary per category ---------------------------------------

summary = df.groupby("Categoria")["Descricao"].count().reset_index()
summary.to_csv("scan_summary.csv", index=False)

print("✔ Scan concluído!")
print("Arquivos gerados: scan_outros.csv, scan_multimatch.csv, scan_summary.csv")
