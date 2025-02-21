from at3_object import AT3Object
from exceptions import ParseException

def _parse_meta(obj: AT3Object, line: str):
    if not line.endswith(']'):
        raise ParseException("meta line must end with ]")


def parse(at3_data: str) -> AT3Object:
    obj = AT3Object()

    lines = at3_data.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("["):
            _parse_meta(obj, line)

    return obj
