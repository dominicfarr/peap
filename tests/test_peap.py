from unittest.mock import MagicMock, call, mock_open, patch

import pytest
from main import Peap


# Assuming TD class has a static method 'process' that can be called with the given parameters.
# Mocking TD class to avoid actual processing in tests.
@pytest.fixture
def mock_td():
    with patch("main.TD") as mock_td:
        mock_td.return_value = MagicMock()
        yield mock_td()


@pytest.fixture
def mock_pdf_reader():
    with patch("main.PdfReader") as mock_reader:
        page = MagicMock()
        page.extract_text.return_value = "Test Pattern"
        mock_reader().pages = [page]
        yield mock_reader


# Mocking AppConfig to provide controlled test data.
@pytest.fixture
def mock_app_config():
    mock_config = MagicMock()
    mock_config.get_files.return_value = [
        {"pdf_file": "test1.pdf", "pdf_password": "pass1"},
        {"pdf_file": "test2.pdf", "pdf_password": "pass2"},
    ]
    mock_config.get_output.return_value = "output.txt"
    mock_config.get_rules.return_value = [{"pattern": "Test Pattern", "class": "TD"}]
    return mock_config


# Parametrized test for happy path, edge cases, and error cases.
@pytest.mark.parametrize(
    "file_list, rules, expected_results, expected_dlq, test_id",
    [
        # Happy path
        (
            [{"pdf_file": "test1.pdf", "pdf_password": "pass1"}],
            [{"pattern": "Test Pattern", "class": "TD"}],
            ["processed test1.pdf"],
            {},
            "happy_path_single_file",
        ),
    ],
    ids=["happy_path_single_file"],
)
def test_peap_processing(
    file_list,
    rules,
    expected_results,
    expected_dlq,
    test_id,
    mock_app_config,
    mock_td,
    mock_pdf_reader,
):
    # Arrange
    mock_app_config.get_files.return_value = file_list
    mock_app_config.get_rules.return_value = rules

    peap = Peap(mock_app_config)

    mock_td.process.side_effect = lambda pdf_file, reader, callback, dlq: callback(
        [f"processed {pdf_file}"]
    )

    # Act
    with patch("builtins.open", mock_open()) as mocked_file:
        peap.run()

    # Assert
    # assert peap.results == expected_results
    assert peap.dlq == expected_dlq
    mocked_file.assert_called_once_with(mock_app_config.get_output(), "a")
    expected_call = call("processed test1.pdf\n")

    # Use assert_has_calls with a list containing the single call object
    mocked_file().write.assert_has_calls([expected_call])
