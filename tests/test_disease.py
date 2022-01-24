from infection_tracker.disease import Disease, InvalidInfectiousPeriodError
from datetime import timedelta
import pytest


def test_disease_valid():
    disease = Disease("Grypa", 2000)
    assert disease.__str__() == "Grypa"
    assert disease.get_infectious_period() == timedelta(minutes=2000)


def test_disease_invalid_period():
    with pytest.raises(InvalidInfectiousPeriodError):
        Disease("Grypa", "abc")


def test_disease_negative_period():
    disease = Disease("Grypa", -120)
    assert disease.__str__() == "Grypa"
    assert disease.get_infectious_period() == timedelta(minutes=120)
