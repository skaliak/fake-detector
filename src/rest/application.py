from flask import Flask, request
from flask_restful import Api, Resource
import logging, sys

sys.path.append("..")
import main.fake_detector as fake_detector
import main.data_layer as data_layer

logging.basicConfig(level=logging.DEBUG, filename='fakedetect_flask.log', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
application = Flask(__name__)
api = Api(application)
detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())

# stub
def detect_fake(username: str) -> bool:
    return detector.is_fake(username)

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

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)