class Person:
    def __init__(self, name: str, surname: str, contact_list = None) -> None:
        self._name = name
        self._surname = surname
        self._contact_list = contact_list

