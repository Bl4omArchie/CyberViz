from cyberviz.hash import compute_hash, compute_hash_from_bytes

from streamlit.runtime.uploaded_file_manager import UploadedFile

from dataclasses import dataclass, field
from pathlib import Path
import tempfile
import logging


@dataclass
class Dataset:
    name: str
    path: str
    size: float
    extension: str
    hash: str


    @staticmethod
    def new_dataset(path: str) -> "Dataset":
        file_path = Path(path)
        if not file_path.is_file():
            logging.warning(f"[!] Path {path} is not a valid file.")
            return None
        
        size_mb = file_path.stat().st_size / (1024 * 1024)
        return Dataset(
            name=file_path.name,
            path=str(file_path),
            size=round(size_mb, 3),
            extension=file_path.suffix.lower().lstrip("."),
            hash=compute_hash(path)
        )


    @staticmethod
    def upload_dataset(dataset: UploadedFile) -> "Dataset":
        try:
            data_bytes = dataset.getvalue()
            size_mb = len(data_bytes) / (1024 * 1024)
            extension = Path(dataset.name).suffix.lower().lstrip(".")
        except Exception as e:
            logging.warning(f"Unable to get metadata : {e}")
            return None

        try:
            suffix = f".{extension}" if extension else ""
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp_file.write(data_bytes)
            tmp_file.flush()
            tmp_file.close()
        except Exception as e:
            logging.warning(f"Unable to upload the file : {e}")
            return None

        return Dataset(
            name=dataset.name,
            path=tmp_file.name,
            size=round(size_mb, 3),
            extension=extension,
            hash=compute_hash_from_bytes(data_bytes)
        )


@dataclass
class CollectionDataset:
    count: int
    size: float
    index: dict = field(default_factory=dict)

    @staticmethod
    def new_collection() -> object:
        return CollectionDataset(index={}, count=0, size=0.0)


    def add_item(self, data: Dataset):
        self.index[data.hash] = data
        self.count += 1
        self.size += data.size

    def delete_item(self, key: str):
        dataset = self.index.pop(key, None)
        if dataset is not None:
            self.count -= 1
            self.size -= dataset.size
