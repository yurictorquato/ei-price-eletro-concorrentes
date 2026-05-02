from pathlib import Path

import pandas as pd

# from IPython.display import display

CAMINHO: Path = Path(r"../../data/input/zvmargens")

# %%

COLUNAS_RENOMEADAS: dict[str, str] = {
    "Org.vendas": "organizacao_vendas",
    "CanalDistr": "canal_distribuicao",
    "Região": "regiao",
    "Loja": "loja",
    "Genérico": "generico",
    "Mercadoria": "mercadoria",
    "Descrição mercadoria": "descricao_mercadoria",
    "UMV": "umv",
    "Preç.Clube": "preco_clube",
    "Preç.Vigen": "preco_vigente",
    "Preç.Promo": "preco_promo",
    "Preç.Pesqu": "preco_pesquisa",
    "PreçNormal": "preco_normal",
    "Preç.Lista": "preco_lista",
    "Tipo Vigen": "tipo_vigente",
    "Iní.Vigent": "inicio_vigente",
    "Fim Vigent": "fim_vigente",
    "Ini. Clube": "inicio_clube",
    "Fim Clube": "fim_clube",
    "PMZ Médio": "pmz_medio",
    "MargVigent": "margem_vigente",
    "MargNormal": "margem_normal",
    "MT%": "margem_teorica",
    "TpPromoção": "tipo_promo",
    "Descrição": "descricao",
    "Data Tipo Vigen": "data_tipo_vigente",
    "Fim Promoç": "fim_promo",
    "AçãoPromo.": "acao_promo",
    "Marg.Pesqu": "margem_pesquisa",
    "MargPromoç": "margem_promo",
    "Status Centro": "status_centro",
    "Estoque": "estoque",
    "Iní.Pesqu.": "inicio_pesquisa",
    "Fim.Pesqu.": "fim_pesquisa",
    "Iní.Normal": "inicio_normal",
    "Iní.Lista": "inicio_lista",
    "Fim Normal": "fim_normal",
    "EAN": "ean",
    "NivPcClube": "nivel_preco_clube",
    "Nív.Pr.Nor": "nivel_preco_normal",
    "Criad.Club": "criado_clube",
    "Criad.Vig": "criado_vigente",
    "PMZ Geren.": "pmz_gerencial",
    "Custo Loja": "custo_loja",
}

COLUNAS_DATAS = [
    "inicio_vigente",
    "fim_vigente",
    "inicio_clube",
    "fim_clube",
    "data_tipo_vigente",
    "fim_promo",
    "inicio_pesquisa",
    "fim_pesquisa",
    "inicio_normal",
    "inicio_lista",
    "fim_normal",
]

COLUNAS_FLOAT = [
    "preco_clube",
    "preco_vigente",
    "preco_promo",
    "preco_pesquisa",
    "preco_normal",
    "preco_lista",
    "pmz_medio",
    "margem_vigente",
    "margem_normal",
    "margem_teorica",
    "margem_pesquisa",
    "margem_promo",
    "pmz_gerencial",
    "custo_loja",
]

COLUNAS_INT = ["estoque"]

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
    
    duplicadas = df.columns.duplicated()

    if duplicadas.any():
        novos_nomes = df.columns.tolist()

        for i, is_dup in enumerate(duplicadas):
            if is_dup:
                novos_nomes[i] = "Data Tipo Vigen"

        df.columns = novos_nomes

    df = df.rename(columns=COLUNAS_RENOMEADAS)

    df = df.apply(
        lambda coluna: (
            coluna.str.strip()
            if coluna.dtype == "str" or coluna.dtype == "object"
            else coluna
        )
    )

    df = df.loc[df["organizacao_vendas"] == "4000", :]

    dataframes.append(df)

df_zvmargens: pd.DataFrame = pd.concat(objs=dataframes, ignore_index=True)

# %%

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
