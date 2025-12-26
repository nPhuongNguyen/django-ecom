import jwt
from apps.catalogue.serializers.token import InfoTokenSerializer
from apps.shared.response import ResponseCodes
def encode_token(data: dict, secret_key: str = None)-> str:
    token = jwt.encode(data, secret_key, algorithm=["HS256"])
    return token

def decode_token(token: str, secret_key: str = None):
    try:
        payload = jwt.decode(token, secret_key,  algorithms=["HS256"])
        serializer = InfoTokenSerializer(data = payload)
        if not serializer.is_valid():
            return None, ResponseCodes.TOKEN_INVALID_TOKEN
        result = serializer.validated_data
        return result, None
    except jwt.ExpiredSignatureError:
        return None, ResponseCodes.TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return None, ResponseCodes.TOKEN_INVALID_TOKEN
    
def normalize_token(token: str)->str|None:
    if not token:
        return None
    parts = token.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    return token



