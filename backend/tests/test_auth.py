from ..auth import verify_password


def test_verify_password(user, password):
    print(user)
    print(user.username)
    print(user.hashed_password)
    assert verify_password(password, user.hashed_password)
    assert not verify_password("", user.hashed_password)
