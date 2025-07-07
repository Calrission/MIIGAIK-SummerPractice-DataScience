import os.path

import pandas as pd

from homeworks.homework_1.constants import OUTPUT_DIR


def prepare():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save(name: str, df: pd.DataFrame) -> str:
    path = os.path.join(OUTPUT_DIR, name)
    csv_content = df.to_csv(index=False, lineterminator='\n').strip()
    with open(path, 'w') as f:
        f.write(csv_content)
    return path
