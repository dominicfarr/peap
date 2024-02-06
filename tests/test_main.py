import json
from io import StringIO
from unittest.mock import Mock, mock_open, patch

import pytest
from config import AppConfig
from main import Peap

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


# Mocking the app_config to provide controlled test data
@pytest.fixture
def mock_app_config():
    mock_config = Mock()
    mock_config.get_files.return_value = [
        {"pdf_file": "test1.pdf", "pdf_password": "password1"},
        {"pdf_file": "test2.pdf", "pdf_password": "password2"}
    ]
    mock_config.get_rules.return_value = [
        {"pattern": "TD Aeroplan Visa", "label": "TD Aeroplan Visa"},
        {"pattern": "Pass The Keys", "label": "Pass The Keys"}
    ]
    return mock_config

# Mocking PdfReader to provide controlled test data
@pytest.fixture
def mock_pdf_reader(mocker):
    return mocker.patch('main.PdfReader', autospec=True)

# Parametrized test for the happy path
@pytest.mark.parametrize(
    "test_id, pdf_text, expected_output",
    [
        ("happy_path_td_visa", "TD Aeroplan Visa\nSTATEMENT PERIOD: January 1,2023toFebruary 1,2023", "test1.pdf is a TD Aeroplan Visa document"),
        ("happy_path_ptk", "Pass The Keys", "test1.pdf is a PTK document"),
        # Add more test cases as needed
    ],
    ids=str,
)
def test_happy_path(mock_app_config, mock_pdf_reader, test_id, pdf_text, expected_output, capsys):
    # Arrange
    peap = Peap(mock_app_config)
    mock_pdf_reader.return_value.pages[0].extract_text.return_value = pdf_text

    # Act
    peap.run()

    # Assert
    captured = capsys.readouterr()
    assert expected_output in captured.out

# Parametrized test for edge cases
@pytest.mark.parametrize(
    "test_id, pdf_text, expected_output",
    [
        ("edge_case_no_statement_period", "TD Aeroplan Visa", ""),
        # Add more edge cases as needed
    ],
    ids=str,
)
def test_edge_cases(mock_app_config, mock_pdf_reader, test_id, pdf_text, expected_output, capsys):
    # Arrange
    peap = Peap(mock_app_config)
    mock_pdf_reader.return_value.pages[0].extract_text.return_value = pdf_text

    # Act
    peap.run()

    # Assert
    captured = capsys.readouterr()
    assert expected_output in captured.out

# Parametrized test for error cases
@pytest.mark.parametrize(
    "test_id, pdf_text, expected_output",
    [
        ("error_case_unknown_document", "Unknown Document", "is in the DLQ"),
        # Add more error cases as needed
    ],
    ids=str,
)
def test_error_cases(mock_app_config, mock_pdf_reader, test_id, pdf_text, expected_output, capsys):
    # Arrange
    peap = Peap(mock_app_config)
    mock_pdf_reader.return_value.pages[0].extract_text.return_value = pdf_text

    # Act
    peap.run()

    # Assert
    captured = capsys.readouterr()
    assert expected_output in captured.out
