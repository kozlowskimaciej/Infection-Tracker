class InvalidInfectiousPeriodError(Exception):
    def __init__(self, period):
        super().__init__(f"{period} is not a valid time.")


class InvalidChoiceError(Exception):
    def __init__(self, choice_num):
        super().__init__(f"{choice_num} is not a valid choice option.")


class InvalidDateError(Exception):
    def __init__(self, date):
        super().__init__(f"{date} is not a valid date.")


class InvalidPersonError(Exception):
    def __init__(self, person):
        super().__init__(f"{person} is not a valid person.")


class InvalidDiseaseError(Exception):
    def __init__(self, disease):
        super().__init__(f"{disease} is not a valid disease.")


class PersonNotExistsError(Exception):
    def __init__(self, person):
        super().__init__(f"{person} does not exist in any meeting.")
