from flask_restful import Resource, request

from .models import LandingPageModel

class LandingPage(Resource):
    def get(self):
        name = request.args.get("name")
        if not name:
            name = "guest"
        return LandingPageModel(name).jsonify(), 201