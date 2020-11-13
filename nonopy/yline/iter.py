def not_none(iterator):
    for element in iterator:
        if element is not None:
            yield element