from datetime import timedelta

class InvalidInfectiousPeriodError(Exception):
    def __init__(self, period):
        super().__init__(f"{period} is not a valid time.") 

class Disease:
    def __init__(self, name: str, infectious_period: int) -> None:
        self._name = str(name)
        try:
            self._infectious_period = timedelta(minutes=infectious_period)
        except TypeError:
            raise InvalidInfectiousPeriodError(infectious_period)

    def get_disease_name(self) -> str:
        return self._name

    def get_infectious_period(self) -> str:
        return self._infectious_period