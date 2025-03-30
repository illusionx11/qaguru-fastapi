
class Server:
    def __init__(self, env):
        self.app = {
            "dev": "http://localhost:8002",
            "beta": "http://localhost:8080",
            "rc": "http://localhost:80"
        }[env]