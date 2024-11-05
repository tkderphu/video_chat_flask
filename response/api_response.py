class APIResponse:
    def __init__(self, message, status, error, data):
        self.message = message
        self.status = status
        self.error = error
        self.data = data

    def to_dict(self):
        return {
            "message": self.message,
            "status": self.status,
            "error": self.error,
            "data": self.data
        }
