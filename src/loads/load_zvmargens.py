# %%

from pathlib import Path

import pandas as pd

# %%

CAMINHO: Path = Path(r"../../data/input/zvmargens")

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
    "tipo_vigente",
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


# %%


def carregar_arquivos_zvmargens() -> pd.DataFrame:
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

        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        df.columns = NOME_COLUNAS

        df = df[~df["organizacao_vendas"].astype(str).str.contains("-", na=False)]

        df = df.apply(lambda x: x.str.strip() if x.dtype == "str" else x)

        df = df[df["organizacao_vendas"] == "4000"]

        dataframes.append(df)

    return pd.concat(objs=dataframes, ignore_index=True).copy()


# %%


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    for coluna in COLUNAS_DATA:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(
                arg=df[coluna], format="%d.%m.%Y", errors="raise"
            )

    for coluna in COLUNAS_NUMERICAS:
        if coluna in df.columns:
            df[coluna] = df[coluna].str.replace(".", "", regex=False)

            df[coluna] = pd.to_numeric(arg=df[coluna], errors="raise")

    return df


# %%

df_zvmargens: pd.DataFrame = carregar_arquivos_zvmargens()

df_zvmargens.dtypes
