from enum import Enum


class DefaultToDoLists(Enum):
    PERSONAL = 'Personal'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_values(cls):
        return [key.value for key in cls]
