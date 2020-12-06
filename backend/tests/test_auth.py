from ..auth import verify_password


def test_verify_password(user, password):
    assert verify_password(password, user.hashed_password)
    assert not verify_password("", user.hashed_password)
