from datetime import timedelta
from infection_tracker.exceptions import InvalidInfectiousPeriodError


class Disease:
    '''
    Class Disease. Conatins attributes:
    :param name: Disease's name
    :type name: str

    :param infectious_period: Disease's infectious period
    :type infectious_period: timedelta
    '''
    def __init__(self, name, infectious_period: int) -> None:
        '''
        Initalizes Disease object
        '''
        self._name = name

        try:
            self._infectious_period = timedelta(
                minutes=abs(int(infectious_period)))
        except Exception:
            raise InvalidInfectiousPeriodError(infectious_period)

    def __str__(self) -> str:
        '''
        Returns disease's name
        '''
        return self._name

    def get_infectious_period(self) -> timedelta:
        '''
        Returns disease's infectious period
        '''
        return self._infectious_period
