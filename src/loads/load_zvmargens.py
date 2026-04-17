# %%

from pathlib import Path

import pandas as pd

CAMINHO: Path = Path(r"../../data/input/zvmargens")


def carregar_arquivos() -> list[pd.DataFrame]:
    dataframes: list[pd.DataFrame] = []

    for arquivo in CAMINHO.glob(pattern="*.txt"):
        df: pd.DataFrame = pd.read_csv(
            filepath_or_buffer=arquivo,
            sep="|",
            encoding="latin1",
            skiprows=3,
            on_bad_lines="skip",
            dtype=str
        )

        df = df.iloc[:, 1:-1]

        # df = df.dropna(axis=1, how="all")
        # df = df.dropna(axis=0, how="all")

        df = df[~df.iloc[:, 0].astype(str).str.contains("-----", na=False)]

        dataframes.append(df)

    return dataframes


daframes: list[pd.DataFrame] = carregar_arquivos()

df_zvmargens: pd.DataFrame = pd.concat(objs=daframes, ignore_index=True)

df_zvmargens
