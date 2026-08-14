from workhub.core.security import (
    create_access_token,
    decode_access_token,
)


def test_create_and_decode_access_token():
    user_id = "123456"
    role = "developer"

    token = create_access_token(
        user_id=user_id,
        role=role,
    )

    payload = decode_access_token(token)

    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert "exp" in payload