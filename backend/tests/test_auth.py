from ..auth import verify_password


def test_verify_password(user, password):
    assert verify_password(password, user.hashed_password)
    assert not verify_password("", user.hashed_password)


def test_api_token(client):
    # assert not authenticated already
    response = client.get("/users/me")
    print(response.status_code)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
    # # get token
    # response = client.post("/token", data={"username": "jochen", "password": "foobar"})
    # assert response.status_code == 200
    # access_token = response.json().get("access_token")
    # assert access_token is not None

    # use fetched token to assert we are authenticated now
    # headers = {"authorization": f"Bearer {access_token}"}
    # response = client.get("/users/me", headers=headers)
    # assert response.status_code == 200
    # print(response.json())
    # assert False