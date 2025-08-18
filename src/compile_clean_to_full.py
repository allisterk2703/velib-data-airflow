import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_DIR = Path("data/station_status/clean")


def compile_all_clean_csvs(data_dir: Path, date_start: datetime, date_end: datetime) -> pd.DataFrame:
    logging.info(f"Scanning all CSVs under {data_dir}/...")

    all_csvs = list(data_dir.glob("**/*.csv"))
    logging.info(f"Found {len(all_csvs)} CSV files before filtering.")

    filtered_csvs = []
    for file in all_csvs:
        try:
            # Extraire la date depuis le nom de fichier: velib_YYYY-MM-DD.csv
            date_str = file.stem.split("_")[1]  # '2025-07-01'
            file_date = datetime.strptime(date_str, "%Y-%m-%d")

            # Vérifier si la date est dans l'intervalle
            if date_start <= file_date <= date_end:
                filtered_csvs.append(file)
        except Exception as e:
            logging.warning(f"Could not parse date for {file}: {e}")

    logging.info(f"{len(filtered_csvs)} CSV files are selected after filtering by date")

    df_list = []
    for file in sorted(filtered_csvs):
        try:
            df = pd.read_csv(
                file,
                dtype={
                    "stationCode": str,
                    "num_bikes_available": int,
                    "num_docks_available": int,
                    "is_working": bool,
                    "num_mechanical_bikes_available": int,
                    "num_ebike_bikes_available": int,
                    "updated_at": str,
                },
            )
            df_list.append(df)
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")

    if not df_list:
        logging.warning("No valid CSVs to compile.")
        return pd.DataFrame()

    df_all = pd.concat(df_list, ignore_index=True)
    df_all = df_all.sort_values(by="updated_at")
    logging.info("All CSV files concatenated.")

    return df_all


if __name__ == "__main__":
    today = datetime.now()

    date_start = (today - timedelta(days=38)).replace(hour=23, minute=55, second=0, microsecond=0)
    date_end = (today - timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0)

    df = compile_all_clean_csvs(DATA_DIR, date_start, date_end)

    if not df.empty:
        df["updated_at"] = pd.to_datetime(df["updated_at"], format="%Y-%m-%d %H:%M:%S")
        output_file = Path("data/station_status/full")
        output_file.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_file / "full_velib_data.parquet", index=False)
        logging.info(f"Saved compiled data to {output_file / 'full_velib_data.parquet'}")
    else:
        logging.warning("No data to save.")

    logging.info(f"Dataframe date start: {df['updated_at'].min()}")
    logging.info(f"Dataframe date end: {df['updated_at'].max()}")

    logging.info(f"Dataframe shape: {df.shape}")
