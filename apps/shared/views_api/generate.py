import uuid

@staticmethod
def generate_code(code=None):
    if code is None:
        code = uuid.uuid4().hex
    return f'{code}-{uuid.uuid4().hex}'