class Date:
    def __init__(self, hour: int, minutes: int, day: int, month: int, year: int) -> None:
        self._minutes = minutes
        self._hour = hour
        self._day = day
        self._month = month
        self._year = year
    
    def __gt__(self, other):
        if self._year == other._year:
            
        elif self._year > other._year:
            return True
        else:
            return False

    def __str__(self):
        return f"{self._hour}:{self._minutes} {self._day}.{self._month}.{self._year}"