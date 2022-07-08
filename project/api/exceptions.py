class ServiceValueError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "Service value can't be empty, {}".format(self.message)
        else:
            return "Service value can't be empty."


class SumValueError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "Sum value must be numeric, {}".format(self.message)
        else:
            return "Sum value must be numeric."


class DateValueError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "Unknown format for date, {}".format(self.message)
        else:
            return "Unknown format for date."


class NumberValueError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "Bill number must be int, {}".format(self.message)
        else:
            return "Bill number must be int."
