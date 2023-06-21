
_info = """
This is an API service that provides Microservices using REST API. Please ensure \
that you refer to the appropriate endpoint based on your specific requirements. \
Make sure to consult the API documentation or relevant resources to identify the \
suitable endpoints for your desired functionalities.\
""".strip()

class LandingPageModel:
    def __init__(self, name):
        self.name = name
        self.info = _info
    def jsonify(self):
        return {"hello": self.name, "info":self.info}