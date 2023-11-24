from locust import HttpUser, task

# N is the number of occurrences of a task.
N = 1

EMAIL = "admin@irontemple.com"
PASSWORD = "00000000pW-"


# HttpUser provides a client for tests
class ProjectPerfTest(HttpUser):
    # @tasks means it is a method to test
    @task
    def get_list_clubs(self):
        self.client.get("/")

    @task(N)
    def get_signup(self):
        self.client.get("/signup/")

    @task(N)
    def get_login(self):
        self.client.get("/login/")

    @task(N)
    def post_login(self):
        self.client.post("/login/", json={"email": EMAIL, "password": PASSWORD})

    @task(N)
    def get_competitions(self):
        self.client.get("/competitions/")

    @task(N)
    def get_reservations(self):
        self.client.get("/reservations/")

    @task(N)
    def get_logout(self):
        self.client.get("/logout/")
