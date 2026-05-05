# %%

from pathlib import Path

import pandas as pd

CAMINHO: Path = Path(r"../../data/input/eiprice_com_frete")


def carregar_arquivos_eiprice_com_frete() -> list[pd.DataFrame]:
    dataframes: list[pd.DataFrame] = []

    for arquivo in CAMINHO.glob(pattern="*.xlsx"):
        df: pd.DataFrame = pd.read_excel(io=arquivo)

        dataframes.append(df)

    return dataframes


dataframes: list[pd.DataFrame] = carregar_arquivos_eiprice_com_frete()

df_com_frete: pd.DataFrame = pd.concat(objs=dataframes, ignore_index=True)

df_com_frete
