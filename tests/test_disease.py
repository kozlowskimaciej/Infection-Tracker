from infection_tracker.disease import Disease, InvalidInfectiousPeriodError
from datetime import timedelta
import pytest


def test_disease_valid():
    disease = Disease("Grypa", 2000)
    assert disease.get_disease_name() == "Grypa"
    assert disease.get_infectious_period() == timedelta(minutes=2000)


def test_disease_invalid_period():
    with pytest.raises(InvalidInfectiousPeriodError):
        Disease("Grypa", "abc")
