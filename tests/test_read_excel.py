from typing import Any
from unittest.mock import patch
import pytest
from src.read_excel import read_excel_file


@patch("pandas.read_excel", return_value=[])
def test_read_excel_file(mock_excel: Any) -> None:
    with patch("os.path.exists", return_value=True):
        assert read_excel_file(" ") == []
    with pytest.raises(ValueError):
        with patch("os.path.exists", return_value=False):
            read_excel_file(" ")
