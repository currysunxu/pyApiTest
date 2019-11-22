import jwt


class JWTHelper:

    @staticmethod
    def decode_token(token, pem_file):
        cert = open(pem_file).read()
        payload = jwt.decode(token, key=cert, verify=False, algorithms=['RS256'])
        return payload
