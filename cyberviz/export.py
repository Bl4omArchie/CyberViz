# Convert a file to parquet format
# Parameter :
#   export_path: folder where your file will be converted
#
def export_to_parquet(export_path: str):
    export_dir = Path(export_path)
    export_dir.mkdir(parents=True, exist_ok=True)

    df = dd.read_csv(self.filepath)
    df.to_parquet(export_dir / file.stem, engine="pyarrow")