from pathlib import Path
from datetime import datetime


def path(file_name):
    return str(
        Path(__file__).parent.joinpath(f'source/{file_name}')
    )

def format_date(year: str, month: str, day: str) -> str:
    date_obj = datetime(int(year), int(month), int(day))
    return date_obj.strftime("%d %B,%Y").lstrip('0')

