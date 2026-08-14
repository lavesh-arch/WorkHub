from workhub.core.security import hash_password, verify_password


def test_password_hashing():
    password = "Admin@12345"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("WrongPassword", password_hash) is False