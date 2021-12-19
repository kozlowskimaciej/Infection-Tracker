from datetime import timedelta

class InvalidInfectiousPeriodError(Exception):
    def __init__(self, period):
        super().__init__(f"{period} is not a valid time.") 

class Disease:
    '''
    Class Disease. Conatins attributes:
    :param name: Disease's name
    :type name: str

    :param infectious_period: Disease's infectious period
    :type infectious_period: timedelta
    '''
    def __init__(self, name: str, infectious_period: int) -> None:
        '''
        Initalizes disease object
        '''
        self._name = str(name)
        try:
            self._infectious_period = timedelta(minutes=infectious_period)
        except TypeError:
            raise InvalidInfectiousPeriodError(infectious_period)

    def get_disease_name(self) -> str:
        '''
        Returns disease's name
        '''
        return self._name

    def get_infectious_period(self) -> str:
        '''
        Returns disease's infectious period
        '''
        return self._infectious_period