from pathlib import Path

import pandas as pd
# from IPython.display import display

CAMINHO: Path = Path(r"../../data/input/zvmargens")

# %%

COLUNAS_DATAS = [
    "Iní.Vigent",
    "Fim Vigent",
    "Ini. Clube",
    "Fim Clube",
    "Tipo Vigen",
    "Fim Promoç",
    "Iní.Pesqu.",
    "Fim.Pesqu.",
    "Iní.Normal",
    "Iní.Lista",
    "Fim Normal",
]

COLUNAS_FLOAT = [
    "Preç.Clube",
    "Preç.Vigen",
    "Preç.Promo",
    "Preç.Pesqu",
    "PreçNormal",
    "Preç.Lista",
    "PMZ Médio",
    "MargVigent",
    "MargNormal",
    "MT%",
    "Marg.Pesqu",
    "MargPromoç",
    "PMZ Geren.",
    "Custo Loja",
]

COLUNAS_INT = ["Estoque"]

# %%

arquivos: list[Path] = list(CAMINHO.glob(pattern="*.txt"))

if not arquivos:
    raise FileNotFoundError(
        f"Nenhum arquivo .txt encontrado na pasta: {CAMINHO.absolute()}"
    )

dataframes: list[pd.DataFrame] = []
for arquivo in arquivos:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=arquivo,
        skiprows=1,
        sep="|",
        encoding="latin1",
        dtype=str,
    )

    df = df.iloc[:, 1:-1]

    df.columns = df.columns.str.strip()

    df = df.loc[df["Org.vendas"] == "4000", :]

    dataframes.append(df)

df_zvmargens: pd.DataFrame = pd.concat(objs=dataframes, ignore_index=True)

# %%

duplicadas = df_zvmargens.columns.duplicated()

if duplicadas.any():
    novos_nomes = df_zvmargens.columns.tolist()

    for i, is_dup in enumerate(duplicadas):
        if is_dup:
            novos_nomes[i] = "Data Tipo Vigen"

df_zvmargens.columns = novos_nomes

df = df.apply(lambda coluna: coluna.str.strip() if coluna.dtype == "str" else coluna)

df[COLUNAS_DATAS] = pd.to_datetime(arg=df[COLUNAS_DATAS], format="%d.%m.%Y")

df[COLUNAS_FLOAT] = df[COLUNAS_FLOAT].astype(float)
df[COLUNAS_INT] = df[COLUNAS_INT].astype(int)


print(df_zvmargens.columns[df_zvmargens.columns.duplicated()])

# %%

print(df_zvmargens.dtypes)
print(df_zvmargens.columns.tolist())
