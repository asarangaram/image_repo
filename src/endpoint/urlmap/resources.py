from flask_restful import Resource


class URLMapResource(Resource):
    @classmethod
    def init_app(cls, app):
        cls.app = app

    def get(self):
        # Extract information from the app's url_map
        endpoints = [rule.endpoint for rule in self.app.url_map.iter_rules()]
        url_map_info = {'endpoints': endpoints}
        return url_map_info
