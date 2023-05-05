from flask import Flask, request
from flask_restful import Api, Resource
import logging, sys, os

import src.main.data_layer as data_layer
import src.main.fake_detector as fake_detector


logging.basicConfig(level=logging.DEBUG, filename='fakedetect_flask.log', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
use_mocks = os.getenv("USE_MOCKS") == "True"
if use_mocks:
    logging.info("Using mocks")
    import src.main.mock_fake_detector as mock_fake_detector
    detector = mock_fake_detector.MockFakeDetector()
else:
    logging.info("Using real detector")
    detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())

application = Flask(__name__)
api = Api(application)

# stub
def detect_fake(username: str) -> bool:
    return detector.is_fake(username)

class UserBio(Resource):
    def get(self, username):
        return {
            'bio': detector.get_user_bio(username),
            'username': username
        }

class Diag(Resource):
    def get(self):
        return os.environ

class Root(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

class FakeDetector(Resource):
    def get(self, username):
        is_fake = detect_fake(username)
        return {'is_fake': is_fake}

class FakeDetectorMulti(Resource):
    # call like this: /fake-detector-multi?u=<username1>&u=<username2>&...
    def get(self):
        usernames = request.args.getlist('u')
        fake_usernames = []
        for username in usernames:
            if detect_fake(username):
                fake_usernames.append(username)
        return {'fake_usernames': fake_usernames}

api.add_resource(FakeDetectorMulti, '/fake-detector-multi')
api.add_resource(FakeDetector, '/fake-detector/<string:username>')
api.add_resource(Root, '/')
api.add_resource(Diag, '/diag')
api.add_resource(UserBio, '/users')

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
