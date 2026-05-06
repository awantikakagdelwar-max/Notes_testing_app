import requests

class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def register(self, email, password):
        requests.post(
            f"{self.base_url}/users/register",
            json={
                "name": "testselenium",
                "email": email,
                "password": password
            }
        )

    def login(self, email, password):
        res = self.session.post(
            f"{self.base_url}/users/login",
            json={
                "email": email,
                "password": password
            }
        )

        print("LOGIN:", res.text)

        self.token = res.json()["data"]["token"]

    @property
    def headers(self):
        return {
            "x-auth-token": self.token,
            "Content-Type": "application/json"
        }