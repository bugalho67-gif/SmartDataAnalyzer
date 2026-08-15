from io import BytesIO

import pandas as pd

from machine_learning.loader import DataLoader


class NamedBytesIO(BytesIO):
    """Buffer com nome de arquivo para simular upload."""

    def __init__(self, content: bytes, name: str) -> None:
        super().__init__(content)
        self.name = name
        self.size = len(content)


def test_loader():
    assert DataLoader is not None


def test_loader_reads_xml_upload() -> None:
    upload = NamedBytesIO(
        b"<root><row><nome>Ana</nome><valor>10</valor></row></root>",
        "dados.xml",
    )

    df = DataLoader.load(upload)

    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "nome"] == "Ana"


def test_loader_preview_resets_file_position() -> None:
    upload = NamedBytesIO(b"nome,valor\nAna,10\nBia,20\n", "dados.csv")
    upload.seek(0)

    preview = DataLoader.preview(upload, rows=1)

    assert len(preview) == 1
    assert upload.tell() == 0
