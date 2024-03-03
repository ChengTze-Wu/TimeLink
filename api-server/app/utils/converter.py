def decamelize(string: str | None) -> str:
    if string is None:
        return None
    return "".join(["_" + i.lower() if i.isupper() else i for i in string]).lstrip("_")
