from pathlib import Path

import pandas as pd

# from IPython.display import display

CAMINHO: Path = Path(r"../../data/input/zvmargens")

# %%

NOME_COLUNAS: list[str] = [
    "organizacao_vendas",
    "canal_distribuicao",
    "regiao",
    "loja",
    "generico",
    "mercadoria",
    "descricao_mercadoria",
    "umv",
    "preco_clube",
    "preco_vigente",
    "preco_promo",
    "preco_pesquisa",
    "preco_normal",
    "preco_lista",
    "tipo_vigente",
    "inicio_vigente",
    "fim_vigente",
    "inicio_clube",
    "fim_clube",
    "pmz_medio",
    "margem_vigente",
    "margem_normal",
    "margem_teorica",
    "tipo_promo",
    "descricao",
    "data_tipo_vigente",
    "fim_promo",
    "acao_promo",
    "margem_pesquisa",
    "margem_promocao",
    "status_centro",
    "estoque",
    "inicio_pesquisa",
    "fim_pesquisa",
    "inicio_normal",
    "inicio_lista",
    "fim_normal",
    "ean",
    "nivel_preco_clube",
    "nivel_preco_normal",
    "criado_clube",
    "criado_vigente",
    "pmz_gerencial",
    "custo_loja",
]

COLUNAS_DATA: list[str] = [
    "inicio_vigente",
    "fim_vigente",
    "inicio_clube",
    "fim_clube",
    "inicio_pesquisa",
    "fim_pesquisa",
    "inicio_normal",
    "inicio_lista",
    "fim_normal",
    "criado_clube",
    "criado_vigente",
]

COLUNAS_NUMERICAS: list[str] = [
    "preco_clube",
    "preco_vigente",
    "preco_promo",
    "preco_pesquisa",
    "preco_normal",
    "preco_lista",
    "pmz_medio",
    "margem_vigente",
    "margem_teorica",
    "margem_pesquisa",
    "margem_promocao",
    "estoque",
    "pmz_gerencial",
    "custo_loja",
]

COLUNAS_NUMERICAS_INT: list[str] = [
    "organizacao_vendas",
    "canal_distribuicao",
    "generico",
    "mercadoria",
    ""
]

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

    df = df.apply(
        lambda coluna: (
            coluna.str.strip()
            if coluna.dtype == "str" or coluna.dtype == "object"
            else coluna
        )
    )

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
            COLUNAS_DATAS.append(novos_nomes[i])

    df_zvmargens.columns = novos_nomes

df_zvmargens[COLUNAS_DATAS] = df_zvmargens[COLUNAS_DATAS].apply(
    lambda coluna: pd.to_datetime(coluna, format="%d.%m.%Y", errors="coerce")
)

df_zvmargens[COLUNAS_FLOAT] = df_zvmargens[COLUNAS_FLOAT].apply(
    lambda coluna: coluna.str.replace(".", "").str.replace(",", ".")
)

df_zvmargens[COLUNAS_FLOAT] = (
    df_zvmargens[COLUNAS_FLOAT]
    .apply(lambda coluna: pd.to_numeric(coluna, errors="coerce"))
    .round(2)
)

df_zvmargens[COLUNAS_INT] = (
    df_zvmargens[COLUNAS_INT]
    .apply(lambda coluna: pd.to_numeric(coluna, errors="coerce"))
    .astype("Int64")
)

# %%

df_zvmargens.to_excel(
    excel_writer="zvmargens_gerado.xlsx", engine="openpyxl", index=False
)
