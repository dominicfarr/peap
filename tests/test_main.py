import json
import pytest
from unittest.mock import patch, mock_open
from io import StringIO
from src.main import Peap, AppConfig

with open("./tests/resources/config.json", "r") as config_file:
    config_data_dict = json.load(config_file)


def test_load_config():
    app_config = AppConfig("./tests/resources/config.json")
    peap = Peap(app_config)

    assert peap.app_config.get_files() == config_data_dict.get("files")
    assert peap.app_config.get_rules() == config_data_dict.get("rules")


def test_is_known_pdf_known_td():
    app_config = AppConfig("./tests/resources/config.json")
    peap = Peap(app_config)

    pdf_text = "This is TD Aeroplan Visa Infinite"
    is_known, label = peap._is_known_pdf(pdf_text)

    assert is_known
    assert label == "TD Aeroplan Visa"


def test_is_known_pdf_known_ptk():
    app_config = AppConfig("./tests/resources/config.json")
    peap = Peap(app_config)

    pdf_text = "PTK"
    is_known, label = peap._is_known_pdf(pdf_text)

    assert is_known
    assert label == "Pass The Keys"


def test_is_known_pdf_unknown():
    app_config = AppConfig("./tests/resources/config.json")
    peap = Peap(app_config)

    pdf_text = "This is an unknown PDF"
    is_known, label = peap._is_known_pdf(pdf_text)

    assert not is_known
    assert label is None
