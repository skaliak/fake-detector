from flask import Flask, request
from flask_restful import Api, Resource
import logging
from src.main import data_layer, fake_detector

app = Flask(__name__)
api = Api(app)
detector = fake_detector(data_layer.HardCodedDataAccess())

# stub
def detect_fake(username: str) -> bool:
    return False

class FakeDetector(Resource):
    def get(self, username):
        is_fake = detect_fake(username)
        return {'is_fake': is_fake}

class FakeDetectorMulti(Resource):
    def get(self):
        usernames = request.args.getlist('username')
        fake_usernames = []
        for username in usernames:
            if detect_fake(username):
                fake_usernames.append(username)
        return {'fake_usernames': fake_usernames}

api.add_resource(FakeDetectorMulti, '/fake-detector-multi')
api.add_resource(FakeDetector, '/fake-detector/<string:username>')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='fakedetect_flask.log', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    app.run(debug=True)
