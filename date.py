class Date:
    def __init__(self, hour: int, minutes: int, day: int, month: int, year: int) -> None:
        self._minutes = minutes
        self._hour = hour
        self._day = day
        self._month = month
        self._year = year
    
    def __ge__(self, other) -> bool:
        if self._year == other._year:
            if self._month == other._month:
                if self._day == other._day:
                    if self._hour == other._hour:
                        if self._minutes >= other._minutes:
                            return True
                        else:
                            return False
                    elif self._hour > other._hour:
                        return True
                    else:
                        return False
                elif self._day > other._day:
                    return True
                else:
                    return False
            elif self._month > other._month:
                return True
            else:
                return False
        elif self._year > other._year:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self._hour}:{self._minutes} {self._day}.{self._month}.{self._year}"