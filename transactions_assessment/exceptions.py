class NonExistError(Exception):
    pass


class WrongExtError(NonExistError):
    pass


class LineFormatError(WrongExtError):
    pass
