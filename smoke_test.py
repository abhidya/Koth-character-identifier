from app import app


def main():
    client = app.test_client()
    health = client.get("/health")
    assert health.status_code == 200
    response = client.post("/results", data={"twittername": "demo"})
    assert response.status_code == 200
    assert b"propane" in response.data


if __name__ == "__main__":
    main()
