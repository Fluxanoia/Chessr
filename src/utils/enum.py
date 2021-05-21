from enum import IntEnum

class ArrayEnum(IntEnum):
    def _generate_next_value_(self, _start, count, _last_values):
        return count

class CountEnum(IntEnum):
    def _generate_next_value_(self, _start, count, _last_values):
        return count + 1

def enum_as_list(enum):
    return [getattr(enum, name) for name in dir(enum) if not name.startswith('_')]
