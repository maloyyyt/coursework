from datetime import datetime

import pandas as pd

from src.reports import search_category


def test_search_category() -> None:
    test_data = {
        "Дата операции": ["2022-01-01", "2022-02-01", "2022-03-01"],
        "Сумма операции": [100, 200, 300],
        "Категория": ["еда", "транспорт", "еда"],
    }
    transactions = pd.DataFrame(test_data)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    result = search_category(transactions, "еда", datetime(2022, 1, 10))
    assert result["category"] == "еда"
    assert result["total"] == -100
