from datetime import timedelta

class Disease:
    def __init__(self, name: str, infectious_period: int) -> None:
        self._name = name
        self._infectious_period = timedelta(minutes=infectious_period)

    def get_disease_name(self) -> str:
        return self._name

    def get_infectious_period(self) -> str:
        return self._infectious_period
    
    def __str__(self) -> str:
        return f"{self._name} has an infectious period of {self._infectious_period}"