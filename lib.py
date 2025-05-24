import sys
from pathlib import Path
from typing import Union
import pandas as pd # type: ignore


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = Path(__file__).parent
    return Path(base_path) / relative_path


def transform_table(
    data: Path, stations_path: Union[Path, None] = None
) -> pd.DataFrame:
    if stations_path is None:
        stations_path = resource_path("Seznam ČS_1_5_2025.xlsx")
    # Load stations info
    stations = pd.read_excel(stations_path, usecols=["č. ČS", "NÁZEV ČS"])

    # Load and clean main data
    df = pd.read_excel(data, engine="xlrd")
    df = df.dropna(how="all")
    df = df.iloc[1:]  # Drop the title row
    df.columns = df.iloc[0]  # Set column names
    df = df.iloc[1:]  # Drop the row used for column names
    df = df.loc[:, df.columns.notna()]
    drop_cols = [
        col for col in ["Zkratka", "Datum", "Agenda", "Doklad"] if col in df.columns
    ]
    df = df.drop(columns=drop_cols)

    # Extract station ID from filename 
    try:
        station_id = int(Path(data).stem.split("_")[0])
    except ValueError:
        raise ValueError(f"Cannot extract station ID from filename: {data}")

    df["č. ČS"] = station_id

    # Add station names
    df = pd.merge(df, stations, on="č. ČS", how="left")

    # Drop last 3 rows that include totals
    df = df.iloc[:-3]

    # Move station info columns to front
    info_cols = ["č. ČS", "NÁZEV ČS"]
    other_cols = [col for col in df.columns if col not in info_cols]
    df = df[info_cols + other_cols]

    # Forward fill Název
    df["Název"] = df["Název"].ffill()
     # Then forward fill EAN within each Název group
    df['EAN'] = df.groupby('Název')['EAN'].ffill()

    # Filter rows with both Množství and Částka
    filtered = df[df["Množství"].notna() & df["Částka"].notna()]

    # Get the last row for each Název group
    sum_rows = filtered.groupby("Název", as_index=False).tail(1).reset_index(drop=True)
    return sum_rows