import pandas as pd


class DataFrameCsvBuilder:
    def __init__(self):
        self.header: list[str] | None = None
        self.rows: list[list[str]] | None = None

    @property
    def is_exist_header(self) -> bool:
        return self.header is not None

    def add_row(self, row: list[str]) -> 'DataFrameCsvBuilder':
        if self.rows is None:
            self.rows = [row]
        else:
            self.rows.append(row)
        return self

    def add_rows(self, rows: list[list[str]]) -> 'DataFrameCsvBuilder':
        if self.rows is None:
            self.rows = rows
        else:
            self.rows += rows
        return self

    def add_header(self, header: list[str]) -> 'DataFrameCsvBuilder':
        self.header = header
        return self

    def build(self) -> pd.DataFrame:
        df = pd.DataFrame(self.rows, columns=self.header)
        return df
