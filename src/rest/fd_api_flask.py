from flask import Flask, request
from flask_restful import Api, Resource
import logging, sys

sys.path.append("..")
import main.fake_detector as fake_detector
import main.data_layer as data_layer

logging.basicConfig(level=logging.DEBUG, filename='fakedetect_flask.log', format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
api = Api(app)
detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())

# stub
def detect_fake(username: str) -> bool:
    return True

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

if __name__ == '__main__':
    logging.getLogger().addHandler(logging.StreamHandler())
    app.run(debug=True)
