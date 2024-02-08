import pytest
from td import TD_Statement_Period


@pytest.mark.parametrize(
    "lines, expected",
    [
        # Happy path tests
        (
            ".\nTD®Aeroplan®Visa Infinite *\nMS MICHELLE ANDERSON 452088XXXXXX1212\nSTATEMENT DATE:January 09,2023 1OF5\nPREVIOUS STATEMENT: December 08,2022\nSTATEMENT PERIOD: December 09,2022toJanuary09,2023",
            {
                "start": "2022-December-09",
                "end": "2023-January-09",
                "is_rollover": True,
            },
        ),
        (
            ".\nTD®Aeroplan®Visa Infinite *\nMS MICHELLE ANDERSON 452088XXXXXX1212\nSTATEMENT DATE:January 09,2023 1OF5\nPREVIOUS STATEMENT: December 08,2022\nSTATEMENT PERIOD: October11,2023toNovember 08,2023",
            {
                "start": "2023-October-11",
                "end": "2023-November-08",
                "is_rollover": False,
            },
        ),
        (
            ".\nTD®Aeroplan®Visa Infinite *\nMS MICHELLE ANDERSON 452088XXXXXX1212\nSTATEMENT DATE:January 09,2023 1OF5\nPREVIOUS STATEMENT: December 08,2022\nSTATEMENT PERIOD: June09,2023toJuly10,2023",
            {"start": "2023-June-09", "end": "2023-July-10", "is_rollover": False},
        ),
    ],
)
def test_parse(lines, expected):
    # Arrange
    td_stat_period = TD_Statement_Period()

    # Act
    result = td_stat_period.get_statement_period(lines)

    # Assert
    assert result["start"] == expected["start"]
    assert result["end"] == expected["end"]
    assert result["is_rollover"]() == expected["is_rollover"]
