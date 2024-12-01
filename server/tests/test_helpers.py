import pytest

from helpers import processing_last_month

def main():
    test_processing_last_month()


def test_processing_last_month():
    assert processing_last_month('01-2023') == '12-2022'
    assert processing_last_month('07-2023') == '06-2023'
    assert processing_last_month('12-2023') == '11-2023'


if __name__ == "__main__":
    main()