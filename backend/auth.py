from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "Veri-X-SIH-26036-SECRET"
ALGORITHM = "HS256"


def create_token(user_id, role):

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )