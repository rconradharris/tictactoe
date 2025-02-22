class ParseException(Exception):
    pass


class ParseStateException(Exception):
    pass


class RequiredFieldMissing(ParseException):
    pass


class UnknownFieldException(ParseException):
    pass
