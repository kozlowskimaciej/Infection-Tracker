from date import Date

def test_two_dates_equal():
    date1 = Date(13, 50, 5, 12, 2021)
    date2 = Date(13, 50, 5, 12, 2021)
    assert (date1 >= date2) == True

def test_two_dates_minutes_bigger():
    date1 = Date(13, 50, 5, 12, 2021)
    date2 = Date(13, 40, 5, 12, 2021) 
    assert (date1 >= date2) == True

def test_two_dates_hours_bigger():
    date1 = Date(14, 50, 5, 12, 2021)
    date2 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == True

def test_two_dates_days_bigger():
    date1 = Date(13, 50, 6, 12, 2021)
    date2 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == True

def test_two_dates_months_bigger():
    date1 = Date(13, 50, 5, 12, 2021)
    date2 = Date(13, 50, 5, 11, 2021) 
    assert (date1 >= date2) == True

def test_two_dates_years_bigger():
    date1 = Date(13, 50, 5, 12, 2022)
    date2 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == True

def test_two_dates_minutes_smaller():
    date2 = Date(13, 50, 5, 12, 2021)
    date1 = Date(13, 40, 5, 12, 2021) 
    assert (date1 >= date2) == False

def test_two_dates_hours_smaller():
    date2 = Date(14, 50, 5, 12, 2021)
    date1 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == False

def test_two_dates_days_smaller():
    date2 = Date(13, 50, 6, 12, 2021)
    date1 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == False

def test_two_dates_months_smaller():
    date2 = Date(13, 50, 5, 12, 2021)
    date1 = Date(13, 50, 5, 11, 2021) 
    assert (date1 >= date2) == False

def test_two_dates_years_smaller():
    date2 = Date(13, 50, 5, 12, 2022)
    date1 = Date(13, 50, 5, 12, 2021) 
    assert (date1 >= date2) == False

def test_date_str():
    date = Date(13, 50, 5, 12, 2021)
    assert date.__str__() == "13:50 5.12.2021"